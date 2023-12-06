import json

import pandas as pd
from google.cloud import bigquery

from infrastructure.infra_config_handler import CONFIG


class BqClient:
    """
    讀取參數建立 BQ Client
    """

    def __init__(self):
        self.project = CONFIG["bigquery"]["project_name"]
        self.client = bigquery.Client(self.project)

    # 執行 SQL 查詢並返回結果的 DataFrame。
    def run_query(self, query):
        """
        針對特定BQ進行SQL查詢

        Args:
            query (str): SQL語法

        Returns:
            df: query回傳的df
        """
        print("WTFFFFF")
        query_job = self.client.query(query)
        # 因為bq的問題，這邊改to_arrow.topandas
        # 另外requirement.txt裡面改pandas==1.2.4
        results = query_job.result()
        print(query_job.state)
        results_dict = [dict(row) for row in results]
        return results_dict
