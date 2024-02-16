import json
from infrastructure.bigquery.client.bq_client import BqClient

class ConfigHandlerTableRepository(BqClient):
    """
    負責從指定的BigQuery表中讀取特定欄位，並將這些欄位的JSON內容轉換成字典。
    """

    def __init__(self, table_path):
        """
        初始化BqTableFieldExtractor實例。

        Args:
            table_path (str): BigQuery表的完整路徑。
        """
        super().__init__()
        self.table_path = table_path

    def extract_field_to_dict(self, field_name, conditions=None):
        """
        從BigQuery表中提取指定欄位的JSON內容，並將其轉換為字典。

        Args:
            field_name (str): 要提取並轉換的欄位名稱。
            conditions (list of str, optional): 查詢條件，用於細化查詢結果。默認為None。

        Returns:
            list of dict: 提取的欄位內容轉換成的字典列表。
        """
        query = f"SELECT `{field_name}` FROM `{self.table_path}`"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        result_data = self.run_query(query)
        extracted_data = [json.loads(row[field_name]) for row in result_data]

        return extracted_data
