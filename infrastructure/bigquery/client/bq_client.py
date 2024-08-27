import json

import pandas as pd
from google.cloud import bigquery
from google.auth import default

# from infrastructure.config_handler import LIAISON_INFRA_CONFIG


class BqClient:
    """
    讀取參數建立 BQ Client
    """

    def __init__(self):
        # 為了避免循環導入，把參數檔的導入移動到內部
        # from infrastructure.config_handler import LIAISON_INFRA_CONFIG
        _, project_id = default()
        self.project = project_id
        # self.project = LIAISON_INFRA_CONFIG["bigquery"]["project_name"]
        # self.client = bigquery.Client(self.project)
        self.client = bigquery.Client()

    # 執行 SQL 查詢並返回結果的 DataFrame。
    def run_query(self, query):
        """
        針對特定BQ進行SQL查詢

        Args:
            query (str): SQL語法

        Returns:
            dict: query回傳的dict
        """
        # print("WTFFFFF")
        print(query)
        query_job = self.client.query(query)
        # 因為bq的問題，這邊改to_arrow.topandas
        # 另外requirement.txt裡面改pandas==1.2.4
        results = query_job.result()
        results_dict = [dict(row) for row in results]
        return results_dict
