from __future__ import annotations

import datetime
import json
import os
import sys

# from contextlib import redirect_stderr
from copy import deepcopy
from dataclasses import dataclass, field, fields
from typing import Any, Callable, overload

import pandas as pd
import requests  # type: ignore
import xarray as xr
from adi_py import Process  # type: ignore
from adi_py.utils import is_empty_function  # type: ignore
from mock import patch  # type: ignore
from wurlitzer import pipes  # type: ignore


@dataclass
class AdiRunner:
    process_name: str

    # TODO: Should these be arguments to run()? If so, then we'd need to handle the
    # input_datasets / output_datasets slightly differently

    site: str
    facility: str
    begin_date: str
    end_date: str

    DATASTREAM_DATA_IN: str | None = field(
        default_factory=lambda: os.getenv("DATASTREAM_DATA_IN"),
        repr=False,
    )
    DATASTREAM_DATA_OUT: str | None = field(
        default_factory=lambda: os.getenv("DATASTREAM_DATA_OUT"),
        repr=False,
    )
    QUICKLOOK_DATA: str | None = field(
        default_factory=lambda: os.getenv("QUICKLOOK_DATA"),
        repr=False,
    )
    LOGS_DATA: str | None = field(
        default_factory=lambda: os.getenv("LOGS_DATA"),
        repr=False,
    )
    CONF_DATA: str | None = field(
        default_factory=lambda: os.getenv("CONF_DATA"),
        repr=False,
    )
    ADI_PY_MODE: str | None = field(
        default_factory=lambda: os.getenv("ADI_PY_MODE"),
        repr=False,
    )

    # Also TODO: is there a way we can send the output data files into the abyss? E.g.,
    # set output data to /dev/null or /tmp or something like that? We have the data in
    # memory, so we don't need it on disk unless the user wants it there.

    # Maybe this should also be in the repr?
    process_class: type[Process] = field(default=Process, repr=False)

    # TODO: Create Protocol/more accurate type hints for each hook function
    init_process_hook: Callable | None = field(default=None, repr=False, kw_only=True)
    pre_retrieval_hook: Callable | None = field(default=None, repr=False, kw_only=True)
    post_retrieval_hook: Callable | None = field(default=None, repr=False, kw_only=True)
    pre_transform_hook: Callable | None = field(default=None, repr=False, kw_only=True)
    post_transform_hook: Callable | None = field(default=None, repr=False, kw_only=True)
    process_data_hook: Callable | None = field(default=None, repr=False, kw_only=True)
    finish_process_hook: Callable | None = field(default=None, repr=False, kw_only=True)
    quicklook_hook: Callable | None = field(default=None, repr=False, kw_only=True)

    def __post_init__(self):
        # Configure ADI Environment variables,
        self._setup_environment_variables()

        self._init_dataset_store()

        self.wrapped_adi_process = create_adi_process(self)
        self.pcm_process = PcmProcess(self.process_name)

        self.input_datastreams = self.pcm_process.input_datastreams
        self.output_datastreams = self.pcm_process.output_datastreams

        # Note: invalid site-facility and date are fed into sys.args and will crash notebook.
        self._validate_date()

    def _init_dataset_store(self):
        self._input_datasets: list[dict[str, xr.Dataset]] = []
        self._output_datasets: list[dict[str, xr.Dataset]] = []
        self._transformed_datasets: list[dict[str, xr.Dataset]] = []

        self._process_intervals: list[tuple[int, int]] = []

        # _input_datasets refactor to tabular
        init_df: pd.DataFrame = pd.DataFrame(
            {
                "datastream": pd.Series(dtype=str),
                "time_start": pd.Series(
                    dtype=object
                ),  # TODO: discuss which timestamp type to use
                "time_end": pd.Series(dtype=object),
                "dataset_id": pd.Series(dtype=int),
                "dataset_info": pd.Series(dtype=object),
            }
        )
        self._input_dataset_table = init_df.copy(deep=True)
        self._output_dataset_table = init_df.copy(deep=True)
        self._transformed_dataset_table = init_df.copy(deep=True)

        self._input_dataset_dict: dict[int, xr.Dataset] = {}
        self._output_dataset_dict: dict[int, xr.Dataset] = {}
        self._transformed_dataset_dict: dict[int, xr.Dataset] = {}

    def _setup_environment_variables(self):
        """Helper function to setup env var,
        Precedence : Valid API, Existing Env Vars, Reasonable Default.
        Then update the instance fields accordingly"""

        adi_env_var_default = {
            "DATASTREAM_DATA_IN": "/data/archive",
            "DATASTREAM_DATA_OUT": f'/data/home/{os.environ["USER"]}/data/datastream',
            "QUICKLOOK_DATA": f'/data/home/{os.environ["USER"]}/data/quicklook',
            "LOGS_DATA": f'/data/home/{os.environ["USER"]}/data/logs',
            "CONF_DATA": f'/data/home/{os.environ["USER"]}/data/conf',
            "ADI_PY_MODE": "development",
        }

        for name, value in adi_env_var_default.items():
            existing_runner_value = getattr(self, name, None)
            if existing_runner_value is not None:
                value = existing_runner_value
            self._validate_environment_variable(name=name, value=value)
            os.environ[name] = value
            setattr(self, name, value)  # update fields

    def _validate_environment_variable(self, name: str, value: str):
        if name == "ADI_PY_MODE":
            adi_py_modes = ["development", "production"]
            if value not in adi_py_modes:
                raise ValueError(
                    f"Invalid env_var {name}={value}. Not in {adi_py_modes}."
                )
        elif name == "DATASTREAM_DATA_IN":
            if not os.access(value, os.R_OK):
                raise ValueError(
                    f"Invalid env_var {name}={value}. Path does not exist or have Read Permissions."
                )
        else:
            if not os.path.exists(value):
                os.makedirs(value, exist_ok=True)
            if not os.access(value, os.W_OK):
                raise ValueError(
                    f"Invalid env_var {name}={value}. Path does not have Write Permissions."
                )

    def _validate_pcm_site_facility(self):
        if (
            self.site.upper(),
            self.facility.upper(),
        ) not in self.pcm_process.site_facilities:
            raise ValueError(
                f"(site, facility): ({self.site}, {self.facility})"
                f"is not in the defined pcm site_facilities {self.pcm_process.site_facilities}. (case-insensitive.)"
            )

    def to_datetime(self, date: str, format: str = "%Y%m%d") -> datetime.datetime:
        try:
            return datetime.datetime.strptime(date, format)
        except ValueError:
            raise ValueError(
                f'Invalid date={date}. Needs to be in the "%Y%m%d" format.(e.g., 20200101.).'
            )

    def _validate_date(self):
        if self.to_datetime(self.begin_date) < datetime.datetime(1992, 1, 1):
            raise ValueError(
                f"begin_date={self.begin_date} is less than the earliest ARM data=19920101."
            )
        if self.to_datetime(self.end_date) < self.to_datetime(self.begin_date):
            raise ValueError(
                f"end_date={self.end_date} is earlier than the begin_date={self.begin_date}."
            )

    def run(self, debug_level: int = 2, show_logs: bool = False) -> ProcessStatus:
        # TODO: add validation to debug_level

        self._init_dataset_store()

        proc_args = (
            ["-n", self.process_name]
            if len(self.wrapped_adi_process.process_names) > 1
            else []
        )
        args = [
            os.path.realpath(__file__),  # not actually needed
            *proc_args,
            "-s",
            self.site,
            "-f",
            self.facility,
            "-b",
            self.begin_date,
            "-e",
            self.end_date,
            "-D",
            f"{debug_level}",
            "-R",
            "--dynamic-dods",
        ]
        with pipes() as (out, _):
            with patch.object(sys, "argv", args):
                self.wrapped_adi_process.run()  # Is a progressbar possible?
        status = ProcessStatus(str(out.read()))
        if show_logs:
            print(status.logs)
        return status
        # TODO: Issue: When wrapped by wurlitzer.pipes and mock.patch, the vscode debugger does not enter the self.wrapped_adi_process.run(), which impedes debugging.
        # and run(show_logs=True) doesn't seem to work.
        # One example is it cannot capture "Lockfile exists: -> /data/home/kefeimo/data/logs/sgp/lockfiles/sgpE13-aoshtdmakappa-VAP.lock" error
        # another example is when AdiRunner(site=.., facility=... ) is not valid, the notebook crashed without informative logs.
        # Use the following block to debug ===========
        # sys.argv = [
        #     "os.path.realpath(__file__)",  # filepath is not actually used
        #     # "-n",
        #     # self.pcm_process,
        #     "-s",
        #     self.site,
        #     "-f",
        #     self.facility,
        #     "-b",
        #     self.begin_date,
        #     "-e",
        #     self.end_date,
        #     "-D",
        #     f"{debug_level}",
        #     "-R",
        #     "--dynamic-dods",
        # ]
        # self.wrapped_adi_process.run()
        # (block stop) Use the following block to debug ===========

    @property
    def input_datasets(self) -> DataStore:
        return DataStore(self._input_datasets, self._process_intervals)

    @property
    def output_datasets(self) -> DataStore:
        return DataStore(self._output_datasets, self._process_intervals)

    @property
    def transformed_datasets(self) -> DataStore:
        return DataStore(self._transformed_datasets, self._process_intervals)


class PcmProcess:
    # TODO: design this wrapper
    """Tracks some information of a PCM Process Definition."""

    def __init__(self, name: str) -> None:
        self.process_name: str = name
        self._process_info: dict = {}

        self._validate_pcm_name()

    def _validate_pcm_name(self):
        if self.process_name not in PcmProcess.get_existing_processes():
            raise ValueError(
                f'PCM process: "{self.process_name}" is not in the records.'
            )

    @property
    def process_info(self) -> dict:
        if self._process_info:
            return self._process_info
        url = f"https://pcm.arm.gov/pcm/api/processes/{self.process_name}"
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Could not connect to PCM Process API {url}")
            raise ConnectionError(f"Could not connect to PCM Process API '{url}'")
        try:
            self._process_info = res.json()["process"]
            return self._process_info
        except:
            print(
                "An error occurred while attempting to interpret the process definition for"
                f" {self.process_name}. Please ensure the process name is valid."
            )
            raise

    @staticmethod
    def get_existing_processes() -> list[str]:
        url = "https://pcm.arm.gov/pcm/api/processes"
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Could not connect to PCM Process API {url}")
            raise ConnectionError(f"Could not connect to PCM Process API '{url}'")
        return list(res.json().keys())

    @property
    def input_datasets(self) -> list[str]:
        process_info = self.process_info
        return list(process_info["variable_retrieval"].keys())

    @property
    def input_datastreams(self) -> list[str]:
        process_info = self.process_info
        return process_info["input_datastreams"]

    @property
    def output_datastreams(self) -> list[str]:
        process_info = self.process_info
        return process_info["output_datastreams"]

    @property
    def run_locations(self) -> list[dict[str, str]]:
        process_info = self.process_info
        return process_info["run_locations"]

    @property
    def site_facilities(self) -> list[tuple[str, str]]:
        return [(location["site"], location["fac"]) for location in self.run_locations]

    @property
    def overview(self) -> pd.DataFrame:
        return self.get_pcm_plans()

    @property
    def input_datastream_priorities(self) -> dict[str, dict[int, str]]:
        priorities = {}
        for input_dataset, rule in zip(
            self.get_input_dataset_rules().input_dataset.values,
            self.get_input_dataset_rules().rules.values,
        ):
            priorities[input_dataset] = {
                x["priority"]: x["datastream_name"] for x in rule
            }
        return priorities

    @property
    def transform_mappings(self) -> dict[str, str]:
        mappings = {}
        for input_dataset, coords in zip(
            self.get_transform_mappings().input_dataset.values,
            self.get_transform_mappings().coordinate_system.values,
        ):
            mappings[input_dataset] = coords
        return mappings

    def get_output_mapping(self) -> pd.DataFrame:
        process = self.process_info
        df_stacked = pd.DataFrame(
            process["variable_retrieval"]["output_datastream_variable_mappings"]
        ).stack()
        df_var_output_mapping = df_stacked.reset_index()
        df_var_output_mapping.columns = [
            "variable",
            "output_datastream",
            "variable_out",
        ]  # non-standard names
        return df_var_output_mapping

    def get_retrieved_variables(self, rich: bool = False) -> pd.DataFrame:
        process = self.process_info
        df_var = pd.DataFrame(process["variable_retrieval"]["retrieved_variables"]).T
        df_var.index.name = "variable"  # non-standard names
        df_var = df_var.reset_index()
        df_var.drop("name", axis=1)
        if rich:
            return df_var
        else:
            return df_var[["variable", "input_dataset", "coordinate_system"]]

    def get_input_dataset_rules(
        self, normalized_datastream: bool = False
    ) -> pd.DataFrame:  # filtered keys, sorted by priority
        process = self.process_info

        def filter_dict(
            datastream: dict,
        ):
            filtered = [
                {
                    key: datastream_dict[key]
                    for key in [
                        "priority",
                        "datastream_name",
                        "run_location",
                        "run_time",
                    ]
                }
                for datastream_dict in datastream
            ]
            return sorted(filtered, key=lambda d: d["priority"])

        def name_list(datastream: dict):  # preserve priority orders
            names = [
                datastream_dict[key]
                for key in ["datastream_name"]
                for datastream_dict in datastream
            ]
            unique_names = []
            for name in names:
                if name not in unique_names:
                    unique_names.append(name)
            return unique_names

        if not normalized_datastream:
            df_input_dataset_rule = (
                pd.DataFrame(process["variable_retrieval"]["input_datasets"])
                .T["rules"]
                .apply(filter_dict)
            )
            df_input_dataset_rule = pd.DataFrame(df_input_dataset_rule)
            df_input_dataset_rule.index.name = "input_dataset"
            df_input_dataset_rule = df_input_dataset_rule.reset_index()
            df_input_dataset_rule["input_datastreams"] = (
                df_input_dataset_rule.rules.apply(name_list)
            )
            return df_input_dataset_rule
        else:
            ser_explode = (
                pd.DataFrame(process["variable_retrieval"]["input_datasets"])
                .T["rules"]
                .apply(filter_dict)
                .explode()
            )
            df_normalized = pd.json_normalize(ser_explode, max_level=0)  # type: ignore
            df_normalized.index = ser_explode.index
            df_normalized.index.name = "input_dataset"
            df_normalized = df_normalized.reset_index()
            return df_normalized

    def get_transform_mappings(self):
        df_rules = self.get_input_dataset_rules()
        df_vars = self.get_retrieved_variables()
        df_mappings = (
            df_vars.groupby("input_dataset")["coordinate_system"]
            .apply(list)
            .reset_index()
        )
        df_mappings["coordinate_system_nona"] = df_mappings.coordinate_system.apply(
            lambda x: [coord for coord in x if coord]
        )
        return pd.merge(
            df_rules,
            df_mappings,
            how="left",
            on="input_dataset",
        )

    def get_pcm_plans(
        self,
        group_by_input_dataset: bool = True,
        show_variable_out: bool = False,
    ) -> pd.DataFrame:
        # process = PcmProcess.get_process_info(process)["process"]
        df_var_non_rich = self.get_retrieved_variables()
        df_output_mapping = self.get_output_mapping()
        df_input_dataset_rules_non_normalized = self.get_input_dataset_rules()

        df_merge_1 = pd.merge(
            df_var_non_rich, df_output_mapping, how="outer", on="variable"
        )
        df_merge_2 = pd.merge(
            df_merge_1,
            df_input_dataset_rules_non_normalized,
            how="outer",
            on="input_dataset",
        )
        df_pcm_plans = pd.merge(
            df_merge_2,
            pd.DataFrame(
                {"output_datastream": self.output_datastreams},
            ),
            how="outer",
        )
        df_pcm_plans = df_pcm_plans.sort_values(
            ["input_dataset", "variable", "coordinate_system", "output_datastream"]
        ).reset_index(drop=True)
        df_pcm_plans = df_pcm_plans[
            [
                "input_dataset",
                "variable",
                "coordinate_system",
                "output_datastream",
                "variable_out",
                "rules",
                "input_datastreams",
            ]
        ]
        if not show_variable_out:
            diffs = df_pcm_plans.variable_out != df_pcm_plans.variable
            if any(diffs):
                df_diff = df_pcm_plans[diffs & df_pcm_plans.variable_out.notna()][
                    ["variable", "variable_out"]
                ]
                print(
                    'Warning: Found non-identical "variable" and "variable_out" names.'
                )
                print(df_diff.to_markdown())
            df_pcm_plans = df_pcm_plans.drop("variable_out", axis=1)
        if group_by_input_dataset:
            tuples = zip(
                df_pcm_plans.input_dataset,
                [str(v) for v in df_pcm_plans.input_datastreams.values],
                df_pcm_plans.index,
            )
            index = pd.MultiIndex.from_tuples(
                tuples,
            )
            df_pcm_plans.index = index
            df_pcm_plans = df_pcm_plans.drop(
                ["input_dataset", "input_datastreams"], axis=1
            )
            return df_pcm_plans
        return df_pcm_plans


class DataStore:
    def __init__(
        self, data: list[dict[str, xr.Dataset]], interval: list[tuple[int, int]] = []
    ):
        self.data = data
        self.interval = interval

    @overload
    def __getitem__(self, key: int) -> dict[str, xr.Dataset]: ...

    @overload
    def __getitem__(self, key: str) -> list[xr.Dataset]: ...

    def __getitem__(self, key: int | str):
        if isinstance(key, int):
            return self.by_interval(key)
        else:
            return self.by_datastream(key)

    @property
    def interval_info(
        self,
    ) -> list[dict[str, int]]:  # {i:..., total:..., start:..., end:...}
        interval_info = []
        for i in range(len(self.interval)):
            info = {}
            info["i"] = i
            info["total"] = len(self.interval) - 1
            info["start"] = self.interval[i][0]
            info["end"] = self.interval[i][1]
            interval_info.append(info)

        return interval_info

    def by_datastream(self, name: str) -> list[xr.Dataset]:
        # return [x[name] for x in self.data]
        return DataSubStore([x[name] for x in self.data], self.interval_info, name)  # type: ignore

    def by_interval(self, index: int) -> dict[str, xr.Dataset]:
        # return self.data[index]
        return DataSubStore(self.data[index], self.interval_info[index], index)  # type: ignore

    def _per_interval_repr(
        self, interval: tuple[int, int], data_dict: dict[str, xr.Dataset]
    ):
        start = datetime.datetime.fromtimestamp(interval[0]).strftime("%Y-%m-%d")
        end = datetime.datetime.fromtimestamp(interval[1]).strftime("%Y-%m-%d")
        time_stamp_line = "\t" + f"{start}--> {end}" + "\t{"

        dataset_lines: list[str] = []
        for datastream, ds in data_dict.items():
            # dim_info = ", ".join([f"{k}: {v}" for k, v in ds.sizes.items()])
            dataset_lines += [
                "\t\t" + f"{datastream}: {XarrayDatasetRepr.one_line_repr(ds)},"
            ]

        close_line = "\t}"

        return [time_stamp_line] + dataset_lines + [close_line]

    def __repr__(self):
        """
        EXAMPLE:
        DataStore
        [
            <0/2> 	2022-01-01--> 2022-01-02	{
                adimappedgrid.c1: xr.Dataset(time: 1440, bound: 2),
                adiregulargrid.c1: xr.Dataset(time: 48, range: 8000, bound: 2),
                nocoord.c1: xr.Dataset(time: 1440, bound: 2),
                nocoord2.c1: xr.Dataset(time: 1440, bound: 2),
            }
            <1/2> 	2022-01-02--> 2022-01-03	{
                adimappedgrid.c1: xr.Dataset(time: 1440, bound: 2),
                adiregulargrid.c1: xr.Dataset(time: 48, range: 8000, bound: 2),
                nocoord.c1: xr.Dataset(time: 1440, bound: 2),
                nocoord2.c1: xr.Dataset(time: 1440, bound: 2),
            }
            <2/2> 	2022-01-03--> 2022-01-04	{
                adimappedgrid.c1: xr.Dataset(time: 1440, bound: 2),
                adiregulargrid.c1: xr.Dataset(time: 48, range: 8000, bound: 2),
                nocoord.c1: xr.Dataset(time: 1440, bound: 2),
                nocoord2.c1: xr.Dataset(time: 1440, bound: 2),
            }
        ]
        """
        open_lines = "DataStore\n["

        dataset_lines = []
        for i, (interval, data) in enumerate(zip(self.interval, self.data)):
            per_interval_repr = self._per_interval_repr(interval, data)
            per_interval_repr[0] = (
                "\t" + f"<{i}/{len(self.interval) - 1}> " + per_interval_repr[0]
            )
            # dataset_lines += per_interval_repr(interval, data)
            if i < 2 or (i == 2 and len(self.interval) <= 3):
                dataset_lines += per_interval_repr
            elif i == len(self.interval) - 1:
                dataset_lines += ["\n\t...\n"]
                dataset_lines += per_interval_repr

        close_line = "]"

        return "\n".join([open_lines] + dataset_lines + [close_line])


class DataSubStore:
    @overload
    def __init__(
        self, slice: list[xr.Dataset], interval_ts: list[dict[str, int]], key: str
    ): ...

    @overload
    def __init__(
        self, slice: dict[str, float], interval_ts: dict[str, int], key: int
    ): ...

    def __init__(self, slice, interval_ts, key):
        self.slice: list[xr.Dataset] | dict[str, xr.Dataset] = slice
        self.interval_info: list[dict[str, int]] | dict[str, int] = interval_ts
        self._slice_repr: list[xr.Dataset] | dict[str, str] | None = None
        self.key: str | int = key
        self._get_repr_()

    @staticmethod
    def _index_timestamp_expression(
        index: int, total: int, start: int, end: int
    ) -> str:
        t_start = datetime.datetime.fromtimestamp(start).strftime("%Y-%m-%d")
        t_end = datetime.datetime.fromtimestamp(end).strftime("%Y-%m-%d")
        return f"<{index}/{total}>" + "\t" + f"{t_start}--> {t_end}"

    def _list_like_repr(self):
        """
        EXAMPLE:
        DataStore (datastream=	co2flx25m_b1)
        [
            <0/4>	2020-04-01--> 2020-04-02	xr.Dataset(time: 48, bound: 2),
            <1/4>	2020-04-02--> 2020-04-03	xr.Dataset(time: 48, bound: 2),

            ...

            <4/4>	2020-04-05--> 2020-04-06	xr.Dataset(time: 48, bound: 2),
        ]
        """
        time_stamp_line = self._index_timestamp_expression(
            self.interval_info["i"],
            self.interval_info["total"],
            self.interval_info["start"],
            self.interval_info["end"],
        )
        open_lines = [f"DataStore (interval=\t{time_stamp_line}) \n" + "{"]
        repr_body = [
            "\t" + f"{datastream}: {XarrayDatasetRepr.one_line_repr(ds)},"
            for datastream, ds in self.slice.items()
        ]
        # type: ignore
        close_line = ["}"]
        return open_lines + repr_body + close_line

    def _dict_like_repr(self):
        """
        EXAMPLE
        DataStore (interval=	<0/4>	2020-04-01--> 2020-04-02)
        {
            co2flx25m_b1: xr.Dataset(time: 48, bound: 2),
            swats_b1: xr.Dataset(time: 48, depth: 6),
        }
        """
        open_lines = [f"DataStore (datastream=\t{self.key}) \n["]
        repr_body = []
        for i, (info, ds) in enumerate(zip(self.interval_info, self.slice)):
            per_interval_repr = [
                "\t"
                + self._index_timestamp_expression(
                    info["i"],
                    info["total"],
                    info["start"],
                    info["end"],
                )
                + "\t"
                + XarrayDatasetRepr.one_line_repr(ds)
                + ","
            ]
            if i < 2 or (i == 2 and len(self.interval_info) <= 3):
                repr_body += per_interval_repr
            elif i == len(self.interval_info) - 1:
                repr_body += ["\n\t...\n"]
                repr_body += per_interval_repr
        close_line = ["]"]
        return open_lines + repr_body + close_line

    def __repr__(self):
        if isinstance(self.slice, dict):
            return "\n".join(self._list_like_repr())
        else:
            return "\n".join(self._dict_like_repr())
        # return self._slice_repr.__repr__()

    def _get_repr_(self):
        if self._slice_repr is not None:
            return
        if isinstance(self.slice, dict):
            self._slice_repr = {}
            for k, v in self.slice.items():  # type: ignore
                self._slice_repr[k] = XarrayDatasetRepr.one_line_repr(v)
        else:  # type(self.slice) is list
            self._slice_repr = []
            for v in self.slice:
                self._slice_repr.append(XarrayDatasetRepr.one_line_repr(v))  # type: ignore


class XarrayDatasetRepr:
    @staticmethod
    def one_line_repr(ds: xr.Dataset):
        dim_info = ", ".join([f"{k}: {v}" for k, v in ds.sizes.items()])
        return f"xr.Dataset({dim_info})"


class PrettyXarrayDataset:
    """
    Pretty printing xr.Dataset
    """

    def __init__(self, ds: xr.Dataset):
        self.ds = ds

    def __repr__(self):
        # return self.dataset_repr(self)
        # self.attrs = super().attrs
        # print("super().attrs")
        # print(super().attrs)
        return (
            "<XarrayDataset>"
            + "("
            + json.dumps(self.get_xrdataset_info(), indent=4)
            + ")"
        )

    def get_xrdataset_info(self):
        # TODO: discuss what other fundamental info should be put here
        ds = self.ds
        attr_dod_version = {"dod_version": ds.attrs["dod_version"]}
        xr_dataset_info: dict = {
            # "time range": (str(ds.time.data[0]).split(".")[0],str(ds.time.data[-1]).split(".")[0]),
            "time range": f'({str(ds.time.data[0]).split(".")[0]}, {str(ds.time.data[-1]).split(".")[0]})',
            "Coordinates": str(list(ds.coords)),
            "Data variables": str(list(ds.data_vars)),
        }
        xr_dataset_info.update(attr_dod_version)
        return xr_dataset_info


class ProcessStatus:
    """Basic class representing the final process state."""

    def __init__(self, logs: str = ""):
        self._logs = logs

    @property
    def succeeded(self) -> bool:
        if self._logs:
            final_log_lines = "\n".join(self._logs.splitlines()[-5:])
        else:
            final_log_lines = ""
        return "successful" in final_log_lines

    @property
    def logs(self) -> str:
        return self._logs

    def __repr__(self) -> str:
        status = "Success" if self.succeeded else "Failed"
        return f"ProcessStatus={status}"

    def __bool__(self) -> bool:
        return self.succeeded


def invoke_parent_hook(
    process: Process,
    runner: AdiRunner,
    hook_name: str,
    *hook_args: Any,
    **hook_kwargs: Any,
) -> None:
    # The hook provided to AdiRunner()
    runner_hook = getattr(runner, hook_name, None)

    # The hook defined in the provided adi_py.Process subclass
    process_class_hook = getattr(runner.process_class, hook_name)

    if runner_hook is None:
        process_class_hook(process, *hook_args, **hook_kwargs)
        return None
    elif not is_empty_function(process_class_hook):  # type: ignore
        class_name = runner.process_class.__class__
        warning_msg = (
            f"Warning! The provided process_class '{class_name}' implements {hook_name}"
            f", but {hook_name} was also provided as an argument to AdiRunner(). The"
            f" AdiRunner() hook will be used, and the {class_name} hook will be"
            " discarded."
        )
        print(warning_msg)
    runner_hook(process, *hook_args, **hook_kwargs)
    return None


def create_adi_process(runner: AdiRunner) -> Process:
    class AdiProcess(runner.process_class):  # type: ignore
        def __init__(self):
            super().__init__()
            if runner.process_class == Process:
                self._process_names = [runner.process_name]
                self._include_debug_dumps = False

        def init_process_hook(self):
            invoke_parent_hook(self, runner, "init_process_hook")

        def pre_retrieval_hook(self, begin_date: int, end_date: int):
            invoke_parent_hook(self, runner, "pre_retrieval_hook", begin_date, end_date)

        def post_retrieval_hook(self, begin_date: int, end_date: int):
            invoke_parent_hook(
                self, runner, "post_retrieval_hook", begin_date, end_date
            )

        def pre_transform_hook(self, begin_date: int, end_date: int):
            invoke_parent_hook(self, runner, "pre_transform_hook", begin_date, end_date)
            interval_data: dict[str, xr.Dataset] = {}
            for (
                input_dataset,
                priorities,
            ) in runner.pcm_process.input_datastream_priorities.items():
                input_datastreams = priorities.values()
                for ds_name in input_datastreams:
                    ds = self.get_retrieved_dataset(
                        ds_name
                    )  # TODO: handle get_retrieved_datasets
                    if ds is not None:
                        ds = ds.copy(deep=True)
                        interval_data[input_dataset] = ds
                        # new_row = pd.DataFrame(
                        #     {
                        #         "datastream": [
                        #             input_dataset
                        #         ],  # TODO: abstract new_row from dict to "pd.row"
                        #         "time_start": [ds.time.data[0]],
                        #         "time_end": [ds.time.data[-1]],
                        #         "dataset_id": [int(id(ds))],
                        #         "dataset_info": [
                        #             PrettyXarrayDataset(ds).get_xrdataset_info()
                        #         ],
                        #     }
                        # )
                        # runner._input_dataset_table = pd.concat(
                        #     [runner._input_dataset_table, new_row], ignore_index=True
                        # )
                        # runner._input_dataset_dict[id(ds)] = ds
                        break
                runner._input_datasets.append(interval_data)
            # TODO: here is the candidate place holder to directly inject custom code,
            # to access it, use runner._input_datasets[index].
            # Note: runner.input_datasets might not be available at this moment,
            # since process_interval is not available until the later process hook.

        def post_transform_hook(self, begin_date: int, end_date: int):
            invoke_parent_hook(
                self, runner, "post_transform_hook", begin_date, end_date
            )
            interval_data: dict[str, xr.Dataset] = {}
            for (
                input_dataset,
                priorities,
            ) in runner.pcm_process.input_datastream_priorities.items():
                input_datastreams = priorities.values()
                for coord_name in runner.pcm_process.transform_mappings[input_dataset]:
                    if not coord_name:
                        continue
                    for ds_name in input_datastreams:
                        ds = self.get_transformed_dataset(
                            ds_name, coord_name
                        )  # TODO: handle get_transformed_datasets
                        if ds is not None:
                            ds = ds.copy(deep=True)
                            interval_data[f"{input_dataset}+=>{coord_name}"] = ds
                            break
                runner._transformed_datasets.append(interval_data)

        def process_data_hook(self, begin_date: int, end_date: int):
            invoke_parent_hook(self, runner, "process_data_hook", begin_date, end_date)
            interval_data: dict[str, xr.Dataset] = {}
            for ds_name in runner.output_datastreams:
                ds = self.get_output_dataset(ds_name)
                if ds is not None:
                    ds = ds.copy(deep=True)
                    interval_data[ds_name] = ds
            runner._output_datasets.append(interval_data)
            runner._process_intervals.append((begin_date, end_date))

        def quicklook_hook(self, begin_date: int, end_date: int):
            invoke_parent_hook(self, runner, "quicklook_hook", begin_date, end_date)

        def finish_process_hook(self):
            invoke_parent_hook(self, runner, "finish_process_hook")

    return AdiProcess()
