import json

from infrastructure.bigquery.client.bq_client import BqClient
from datetime import datetime
from infrastructure.infra_config_handler import CONFIG


class RawTableRepository(BqClient):
    """
    負責涉及 clean_job 表格的操作
    """

    def __init__(self, raw_table_path):
        super().__init__()
        # self.bigquery_table_id = f"{self.project}.{self.dataset}.{self.table}"
        self.bigquery_table_id = raw_table_path

    def save(self, raw_table):
        """
        把 raw_table 存到bq

        Args:
            raw_table (raw_table實體)
        """
        raw_table_dict = self.__convert_raw_table_to_bq_format(raw_table)
        insertion_errors = self.client.insert_rows_json(
            self.bigquery_table_id, [raw_table_dict]
        )
        if insertion_errors:
            print(
                f"Errors occurred while storing Raw Table to BigQuery: {insertion_errors}"
            )
        else:
            print(
                "Raw Table stored successfully to BigQuery."
            )

    def __convert_raw_table_to_bq_format(self, raw_table):
        """
        把 raw_table 轉換成可以存入BQ的格式

        Args:
            raw_table (raw_table 實體)

        Returns:
            dict: 可存入BQ的格式
        """
        # 將 datetime 對象轉換為 RFC 3339 格式的字符串
        # start_time_str = raw_table.START_TIME.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        # end_time_str = raw_table.END_TIME.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        bq_created_time = datetime.now()
        bq_created_time_str = bq_created_time.strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        bq_updated_time_str = bq_created_time.strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        # 創建一個字典，並確保每個值都符合格式
        bq_dict = {
            "UUID_Request": str(raw_table.UUID_Request),
            "MISSION_NAME": str(raw_table.MISSION_NAME),
            "TASK_NAME": str(raw_table.TASK_NAME),
            "RAW_DATA": str(raw_table.RAW_DATA),
            "BQ_CREATED_TIME": bq_created_time_str,
            "BQ_UPDATED_TIME": bq_updated_time_str,
        }
        return bq_dict
