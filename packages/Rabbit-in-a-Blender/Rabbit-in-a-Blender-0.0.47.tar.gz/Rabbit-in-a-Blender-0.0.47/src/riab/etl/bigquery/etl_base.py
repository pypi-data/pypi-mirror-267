# Copyright 2024 RADar-AZDelta
# SPDX-License-Identifier: gpl3+

# pylint: disable=unsubscriptable-object
"""Holds the BigQuery ETL base class"""

import json
import logging
from abc import ABC
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, List, Optional, cast

import google.auth
import google.cloud.bigquery as bq
import pyarrow as pa
import pyarrow.parquet as pq

from ..etl_base import EtlBase
from .gcp import Gcp


class BigQueryEtlBase(EtlBase, ABC):
    def __init__(
        self,
        credentials_file: Optional[str],
        location: Optional[str],
        project_raw: Optional[str],
        dataset_work: str,
        dataset_omop: str,
        dataset_dqd: str,
        dataset_achilles: str,
        bucket: str,
        **kwargs,
    ):
        """This class holds the BigQuery specific methods of the ETL process

        Args:
            credentials_file (Optional[str]): The credentials file must be a service account key, stored authorized user credentials, external account credentials, or impersonated service account credentials. (see https://google-auth.readthedocs.io/en/master/reference/google.auth.html#google.auth.load_credentials_from_file), Alternatively, you can also use 'Application Default Credentials' (ADC) (see https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login)
            location (Optional[str]): Location where to run the BigQuery jobs. Must match the location of the datasets used in the query. (important for GDPR)
            project_raw (Optional[str]): Can be handy if you use jinja templates for your ETL queries (ex if you are using development-staging-production environments). Must have the following format: PROJECT_ID
            dataset_work (str): The dataset that will hold RiaB's housekeeping tables. Must have the following format: PROJECT_ID.DATASET_ID
            dataset_omop (str): The dataset that will hold the OMOP table. Must have the following format: PROJECT_ID.DATASET_ID
            bucket (str): The Cloud Storage bucket uri, that will hold the uploaded Usagi and custom concept files. (the uri has format 'gs://{bucket_name}/{bucket_path}')
        """
        super().__init__(**kwargs)

        if credentials_file:
            credentials, project_id = google.auth.load_credentials_from_file(credentials_file)
        else:
            credentials, project_id = google.auth.default()

        self._gcp = Gcp(credentials=credentials, location=location or "EU")
        self._project_raw = cast(str, project_raw)
        self._dataset_work = dataset_work
        self._dataset_omop = dataset_omop
        self._dataset_dqd = dataset_dqd
        self._dataset_achilles = dataset_achilles
        self._bucket_uri = bucket

        self.__clustering_fields = None

    def __exit__(self, exception_type, exception_value, exception_traceback):
        logging.info("Total BigQuery cost: %s€", self._gcp.total_cost)
        EtlBase.__exit__(self, exception_type, exception_value, exception_traceback)

    @property
    def _clustering_fields(self) -> Dict[str, List[str]]:
        """The BigQuery clustering fields for every OMOP table

        Returns:
            Dict[str, List[str]]: A dictionary that holds for every OMOP table the clustering fields.
        """
        if not self.__clustering_fields:
            with open(
                str(
                    Path(__file__).parent.resolve()
                    / "templates"
                    / "ddl"
                    / f"OMOPCDM_bigquery_{self._omop_cdm_version}_clustering_fields.json"
                ),
                "r",
                encoding="UTF8",
            ) as file:
                self.__clustering_fields = json.load(file)
        return self.__clustering_fields

    def _upload_arrow_table(self, table: pa.Table, dataset: str, table_name: str):
        with TemporaryDirectory(prefix="riab_") as tmp_dir:
            tmp_file = str(Path(tmp_dir) / f"{table_name}.parquet")
            logging.debug("Writing arrow table to parquet file '{tmp_file}'")
            pq.write_table(table, where=tmp_file)

            # upload the Parquet file to the Cloud Storage Bucket
            uri = self._gcp.upload_file_to_bucket(tmp_file, self._bucket_uri)
            # load the uploaded Parquet file from the bucket into the specific standardised vocabulary table
            self._gcp.batch_load_from_bucket_into_bigquery_table(
                uri,
                dataset,
                table_name,
                write_disposition=bq.WriteDisposition.WRITE_APPEND,
            )

    def _get_column_type(self, cdmDatatype: str) -> str:
        match cdmDatatype:
            case "integer":
                return "int64"
            case "datetime":
                return "datetime"
            case "varchar(50)":
                return "string"
            case "date":
                return "date"
            case "datetime":
                return "datetime"
            case "Integer":
                return "int64"
            case "varchar(20)":
                return "string"
            case "float":
                return "float64"
            case "varchar(MAX)":
                return "string"
            case "varchar(255)":
                return "string"
            case "varchar(10)":
                return "string"
            case "varchar(60)":
                return "string"
            case "varchar(250)":
                return "string"
            case "varchar(1)":
                return "string"
            case "varchar(2000)":
                return "string"
            case "varchar(2)":
                return "string"
            case "varchar(9)":
                return "string"
            case "varchar(80)":
                return "string"
            case "varchar(3)":
                return "string"
            case "varchar(25)":
                return "string"
            case "varchar(1000)":
                return "string"
            case _:
                raise ValueError(f"Unknown cdmDatatype: {cdmDatatype}")
