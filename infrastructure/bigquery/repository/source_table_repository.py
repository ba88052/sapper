import json

from infrastructure.bigquery.client.bq_client import BqClient
from datetime import datetime
from infrastructure.infra_config_handler import CONFIG


class SourceTableRepository(BqClient):
    """
    負責涉及 clean_job 表格的操作
    """

    def __init__(self, source_table_path):
        super().__init__()
        # self.bigquery_table_id = f"{self.project}.{self.dataset}.{self.table}"
        self.bigquery_table_id = source_table_path

    def customize_select(self, conditions=None):
        """
        把 raw_table 存到bq

        Args:
            raw_table (raw_table實體)
        """
         # 基本查詢
        query = f"SELECT * FROM `{self.bigquery_table_id}`"

        # 添加條件
        if conditions:
            query += " WHERE " + " ".join(conditions)
        print(query)
        result_data =  self.run_query(query)
        rows = [dict(row) for row in result_data]  # 將每行數據轉換為字典
        json_data = json.dumps(rows)  # 將字典列表轉換為 JSON 字符串

        return json_data