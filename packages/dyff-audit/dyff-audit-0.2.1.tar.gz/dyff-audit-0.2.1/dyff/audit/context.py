# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

# mypy: disable-error-code="import-untyped"
import os
from pathlib import Path
from typing import Iterable, Optional, TypeVar

import pyarrow
import ruamel.yaml

from dyff.client import Client
from dyff.schema import ids
from dyff.schema.dataset import arrow
from dyff.schema.platform import Analysis, MethodInputKind

T = TypeVar("T")


def _once(x: T) -> Iterable[T]:
    yield x


def _analysis_from_yaml(analysis_yaml: dict) -> Analysis:
    spec = analysis_yaml["spec"]
    spec["method"]["id"] = ids.null_id()
    spec["method"]["account"] = ids.null_id()
    return Analysis.parse_obj(spec)


class AnalysisContext:
    def __init__(
        self,
        *,
        id: Optional[str] = None,
        analysis: Optional[Analysis] = None,
        analysis_config_file: Optional[str] = None,
        local_storage_root: Optional[str] = None,
        use_remote: bool = False,
        api_endpoint: Optional[str] = None,
        api_token: Optional[str] = None,
        no_verify_ssl_certificates: bool = False,
    ):
        if id is not None and analysis is not None:
            if analysis_config_file is not None:
                raise ValueError(
                    "'(id, analysis)' and 'analysis_config_file' are mutually exclusive"
                )
            self._id = id
            self._analysis = analysis
        else:
            analysis_config_file = analysis_config_file or os.environ.get(
                "DYFF_AUDIT_ANALYSIS_CONFIG_FILE"
            )
            if analysis_config_file is None:
                raise ValueError(
                    "Must provide '(id, analysis)' or 'analysis_config_file'"
                    " or set DYFF_AUDIT_ANALYSIS_CONFIG_FILE environment variable"
                )
            if id is not None or analysis is not None:
                raise ValueError(
                    "'(id, analysis)' and 'analysis_config_file' are mutually exclusive"
                )

            yaml = ruamel.yaml.YAML()
            with open(analysis_config_file, "r") as fin:
                analysis_yaml = yaml.load(fin)
            self._id = analysis_yaml["spec"]["id"]
            self._analysis = _analysis_from_yaml(analysis_yaml)

        local_storage_root = local_storage_root or os.environ.get(
            "DYFF_AUDIT_LOCAL_STORAGE_ROOT"
        )
        if local_storage_root is None:
            raise ValueError(
                "Must provide local_storage_root"
                " or set DYFF_AUDIT_LOCAL_STORAGE_ROOT environment variable."
            )
        self._local_storage_root = Path(local_storage_root)
        if not self._local_storage_root.is_absolute():
            raise ValueError("local_storage_root must be an absolute path")

        self._use_remote = use_remote or (
            os.environ.get("DYFF_AUDIT_USE_REMOTE") == "1"
        )
        self._api_endpoint = (
            api_endpoint
            or os.environ.get("DYFF_API_ENDPOINT")
            or "https://api.dyff.io/v0"
        )
        self._api_token = api_token or os.environ.get("DYFF_API_TOKEN")
        self._no_verify_ssl_certificates = no_verify_ssl_certificates or (
            os.environ.get("DYFF_API_NO_VERIFY_SSL_CERTIFICATES") == "1"
        )

        self._client: Optional[Client] = None
        if self._use_remote:
            if self._api_token is None:
                raise ValueError(
                    "API token not specified; set use_remote=False to disable remote access"
                )
            self._client = Client(
                api_key=self._api_token,
                endpoint=self._api_endpoint,
                verify_ssl_certificates=(not self._no_verify_ssl_certificates),
            )

        self._parameters = {p.keyword: p for p in self.analysis.method.parameters}
        self._arguments = {a.keyword: a.value for a in self.analysis.arguments}
        self._inputs = {i.keyword: i.entity for i in self.analysis.inputs}
        self._input_kinds = {i.keyword: i.kind for i in self.analysis.method.inputs}
        self._input_paths = {
            e.keyword: str(self._local_storage_root / e.entity)
            for e in self.analysis.inputs
        }

    @property
    def analysis(self) -> Analysis:
        return self._analysis

    @property
    def local_storage_root(self) -> Path:
        return self._local_storage_root

    @property
    def output_path(self) -> Path:
        return self._local_storage_root / self._id

    @property
    def arguments(self) -> dict[str, str]:
        return self._arguments.copy()

    @property
    def inputs(self) -> list[str]:
        return list(self._inputs.keys())

    def get_argument(self, keyword: str) -> str:
        return self._arguments[keyword]

    def open_input_dataset(self, keyword: str) -> pyarrow.dataset.Dataset:
        entity = self._inputs[keyword]
        path = self._local_storage_root / entity
        if not path.is_dir():
            if self._client:
                path.mkdir()
                self._download_data(self._input_kinds[keyword], entity, path)
            else:
                raise ValueError(
                    f'Entity {entity} ("{keyword}") not found locally and remote API is unavailable'
                )
        return arrow.open_dataset(str(path))

    def _download_data(self, kind: MethodInputKind, id: str, path: Path):
        assert self._client is not None
        if kind == MethodInputKind.Dataset:
            dataset = self._client.datasets.get(id)
            dataset_data = self._client.datasets.data(dataset)
            arrow.write_dataset(
                dataset_data.to_batches(),
                output_path=str(path),
                feature_schema=dataset_data.dataset_schema,
                existing_data_behavior="error",
            )
        elif kind == MethodInputKind.Evaluation:
            raise NotImplementedError()
        elif kind == MethodInputKind.Measurement:
            raise NotImplementedError()
        elif kind == MethodInputKind.Report:
            report = self._client.reports.get(id)
            report_data = self._client.reports.data(report)
            record_batch = pyarrow.RecordBatch.from_pandas(report_data)
            arrow.write_dataset(
                _once(record_batch),
                output_path=str(path),
                feature_schema=record_batch.schema,
                existing_data_behavior="error",
            )
        else:
            raise ValueError(f"MethodInputKind {kind}")
