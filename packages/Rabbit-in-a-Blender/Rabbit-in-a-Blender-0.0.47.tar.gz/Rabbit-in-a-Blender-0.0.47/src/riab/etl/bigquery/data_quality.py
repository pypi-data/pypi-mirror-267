# Copyright 2024 RADar-AZDelta
# SPDX-License-Identifier: gpl3+

import logging
import traceback
from time import time
from typing import Any, List, Optional

import polars as pl
import pyarrow as pa

from ..data_quality import DataQuality
from .etl_base import BigQueryEtlBase


class BigQueryDataQuality(DataQuality, BigQueryEtlBase):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def _run_check_query(
        self, check: Any, row: str, parameters: Any, cohort_definition_id: Optional[int] = None
    ) -> Any:
        sql = None
        result = None
        exception: str | None = None
        execution_time = -1
        try:
            parameters["cdmDatabaseSchema"] = self._dataset_omop
            parameters["cohortDatabaseSchema"] = self._dataset_omop
            parameters["cohortTableName"] = "cohort"
            parameters["cohortDefinitionId"] = cohort_definition_id
            parameters["vocabDatabaseSchema"] = self._dataset_omop
            parameters["cohort"] = "TRUE" if cohort_definition_id else "FALSE"
            parameters["schema"] = self._dataset_omop

            sql = self._render_sqlfile(check["sqlFile"], parameters)

            start = time()
            rows = self._gcp.run_query_job(sql)
            end = time()
            execution_time = end - start
            result = dict(next(rows))
        except Exception as ex:
            logging.warn(traceback.format_exc())
            exception = str(ex)
            # if __debug__:
            #     breakpoint()

        return self._process_check(check, row, parameters, sql, result, execution_time, exception)

    def _get_cdm_sources(self) -> List[Any]:
        """Merges the uploaded custom concepts in the OMOP concept table.

        Returns:
            RowIterator | _EmptyRowIterator: The result rows
        """
        template = self._template_env.from_string("select * from {{dataset_omop}}.cdm_source;")
        sql = template.render(
            dataset_omop=self._dataset_omop,
        )
        rows = self._gcp.run_query_job(sql)
        return [dict(row.items()) for row in rows]

    def _store_dqd_run(self, dqd_run: dict):
        table = pa.Table.from_pylist([dqd_run])
        # df = pl.from_dicts([dqd_run])
        self._upload_arrow_table(table, self._dataset_dqd, "dqdashboard_runs")

    def _store_dqd_result(self, dqd_result: pl.DataFrame):
        dqd_result.with_columns(
            [
                pl.col("num_violated_rows").replace(None, 0).alias("num_violated_rows"),
                pl.col("num_denominator_rows").replace(None, 0).alias("num_denominator_rows"),
                pl.col("threshold_value").replace(None, 0).alias("threshold_value"),
            ]
        )
        table = dqd_result.to_arrow()
        self._upload_arrow_table(table, self._dataset_dqd, "dqdashboard_results")
