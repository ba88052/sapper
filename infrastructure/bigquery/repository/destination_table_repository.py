import json

from infrastructure.bigquery.client.bq_client import BqClient
from datetime import datetime
from infrastructure.infra_config_handler import CONFIG


class DestinationTableRepository(BqClient):
    """
    負責涉及 clean_job 表格的操作
    """

    def __init__(self, destination_table_path):
        super().__init__()
        # self.bigquery_table_id = f"{self.project}.{self.dataset}.{self.table}"
        self.bigquery_table_id = destination_table_path

    def save(self, destination_data_dict):
        """
        把 raw_table 存到bq

        Args:
            raw_table (raw_table實體)
        """
        destination_data_dict = self.__compare_and_fill_destination_table(destination_data_dict)
        destination_data_dict = self.__convert_to_bq_format(destination_data_dict)
        insertion_errors = self.client.insert_rows_json(
            self.bigquery_table_id, [destination_data_dict]
        )
        if insertion_errors:
            print(
                f"Errors occurred while storing destination_data_dict to BigQuery: {insertion_errors}"
            )
        else:
            print(
                "destination_data_dict stored successfully to BigQuery."
            )

    def __get_table_schema(self, table_id):
        # 獲取 BigQuery 表的 schema
        table = self.client.get_table(table_id)
        schema_field_names = {field.name for field in table.schema}
        return schema_field_names
    
    def __compare_and_fill_destination_table(self, table_id, json_data):
        schema_field_names = self.__get_table_schema(table_id)
        # 比對 JSON 資料與 schema，填充缺失的欄位
        filled_data = []
        for record in json_data:
            filled_record = {field: record.get(field, "") for field in schema_field_names}
            filled_data.append(filled_record)
        return filled_data

    def __convert_to_bq_format(self, destination_data_dict):
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
            "UUID_Request": str(destination_data_dict["UUID_Request"]),
            "MISSION_NAME": str(destination_data_dict["MISSION_NAME"]),
            "TASK_NAME": str(destination_data_dict["TASK_NAME"]),
            "RAW_DATA": str(destination_data_dict["RAW_DATA"]),
            "BQ_CREATED_TIME": bq_created_time_str,
            "BQ_UPDATED_TIME": bq_updated_time_str,
        }
        return bq_dict
