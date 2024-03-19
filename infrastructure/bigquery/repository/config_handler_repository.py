import json
from infrastructure.bigquery.client.bq_client import BqClient

class ConfigHandlerRepository(BqClient):
    """
    負責從指定的BigQuery表中讀取特定欄位，並將這些欄位的JSON內容轉換成字典。
    """

    def __init__(self, table_path):
        """
        初始化ConfigHandlerRepository實例。

        Args:
            table_path (str): BigQuery表的完整路徑。
        """
        super().__init__()
        self.table_path = table_path

    def extract_last_config(self, field_name, conditions=None):
        """
        從BigQuery表中提取指定欄位的JSON內容，並將其轉換為字典。

        Args:
            field_name (str): 要提取並轉換的欄位名稱。
            conditions (list of str, optional): 查詢條件，用於細化查詢結果。默認為None。

        Returns:
            dict or None: 提取的欄位內容轉換成的字典，如果沒有結果則返回None。
        """
        # 修改查詢，以便按BQ_UPDATED_TIME降序排序，並僅返回最新的一條記錄
        query = f"SELECT `{field_name}` FROM `{self.table_path}`"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY BQ_UPDATED_TIME DESC LIMIT 1"  # 按BQ_UPDATED_TIME降序排序並限制結果為1

        result_data = self.run_query(query)
        # 由於僅返回最新一條記錄，因此直接處理單個結果，如果查詢結果為空，則返回空字典
        extracted_data = json.loads(result_data[0][field_name]) if result_data else None
        # print(extracted_data)

        return extracted_data
