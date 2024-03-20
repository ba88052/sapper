import json
from datetime import datetime, timezone

from infrastructure.bigquery.client.bq_client import BqClient
from infrastructure.config_handler import INFRA_CONFIG


class FLowLogRepository(BqClient):
    """
    負責涉及 flow_log 表格的操作
    """

    def __init__(self):
        super().__init__()
        self.dataset = INFRA_CONFIG["bigquery"]["log"]["dataset_name"]
        self.table = INFRA_CONFIG["bigquery"]["log"]["flow_log_table_name"]
        self.bigquery_table_id = f"{self.project}.{self.dataset}.{self.table}"

    def save(self, flow_log):
        """
        flow_log 存到bq

        Args:
            flow_log (flow_log)
        """
        flow_log_dict = self.__convert_flow_log_entity_to_bq_format(flow_log)

        print(flow_log_dict)

        insertion_errors = self.client.insert_rows_json(
            self.bigquery_table_id, [flow_log_dict]
        )
        if insertion_errors:
            print(
                f"Errors occurred while storing flow_log to BigQuery: {insertion_errors}"
            )
        else:
            print("flow_log stored successfully to BigQuery.")

    def __get_table_schema(self, table_id):
        """
        # 獲取 BigQuery 表的 schema

        Args:
            table_id (str): 目標表的ID，或者說路徑

        Returns:
            dict: 目標表的schema dict
        """

        table = self.client.get_table(table_id)
        schema_field_names = {field.name for field in table.schema}
        print("schema", schema_field_names)
        return schema_field_names

    def __convert_flow_log_entity_to_bq_format(self, flow_log):
        """
        把entity轉換成可以存入BQ的格式

        Args:
            flow_log (flow_log實體)

        Returns:
            dict: 可存入BQ的格式
        """
        # # 將 datetime 對象轉換為 RFC 3339 格式的字符串
        bq_created_time = datetime.now()
        bq_created_time_utc = bq_created_time.replace(tzinfo=timezone.utc)
        bq_created_time_str = bq_created_time_utc.isoformat()
        bq_created_time_str = bq_created_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        bq_updated_time_str = bq_created_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        flow_log.BQ_CREATED_TIME = bq_created_time_str
        flow_log.BQ_UPDATED_TIME = bq_updated_time_str
        # 創建一個字典，並確保每個值都符合格式
        flow_log_dict = vars(flow_log)
        schema_field_names = self.__get_table_schema(self.bigquery_table_id)
        filled_data = {}
        for field in schema_field_names:
            # 如果該欄位在 destination_data 中存在，則使用其值，否則使用預設值 ""
            filled_data[field] = flow_log_dict.get(field, "")
        return filled_data
