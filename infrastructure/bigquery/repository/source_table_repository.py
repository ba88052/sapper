import json
from datetime import datetime

from infrastructure.bigquery.client.bq_client import BqClient
from infrastructure.config_handler import INFRA_CONFIG


class SourceTableRepository(BqClient):
    """
    負責涉及 source table 表格的操作
    """

    def __init__(self, source_table_path):
        super().__init__()
        self.bigquery_table_id = source_table_path

    def customize_select(self, conditions=None):
        """
        從 source table 中使用sql客製化select資料

        Args:
            raw_table (raw_table實體)
        """
        # 基本查詢
        query = f"SELECT * FROM `{self.bigquery_table_id}`"

        # 添加條件
        if conditions:
            query += " WHERE " + " ".join(conditions)
        result_data = self.run_query(query)

        return result_data
