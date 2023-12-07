import json

from infrastructure.bigquery.client.bq_client import BqClient
from datetime import datetime, timezone
from infrastructure.infra_config_handler import CONFIG


class DestinationTableRepository(BqClient):
    """
    負責涉及 clean_job 表格的操作
    """

    def __init__(self, destination_table_path):
        super().__init__()
        # self.bigquery_table_id = f"{self.project}.{self.dataset}.{self.table}"
        self.bigquery_table_id = destination_table_path

    def save(self, general_tmp_data_entity, use_tmp_table):
        """
        把 raw_table 存到bq

        Args:
            raw_table (raw_table實體)
        """
        if use_tmp_table == True:
            general_tmp_data_dict = self.__convert_to_tmp_table_format(general_tmp_data_entity)
            insertion_errors = self.client.insert_rows_json(
                self.bigquery_table_id, [general_tmp_data_dict]
                )
            if insertion_errors:
                print(
                    f"Errors occurred while storing destination_data_dict to BigQuery: {insertion_errors}"
                )
            else:
                print(
                    "destination_data_dict stored successfully to BigQuery."
                )
        else:
            for destination_data in general_tmp_data_entity.TMP_DATA:
                destination_data_dict = self.__convert_to_destination_table_format(destination_data)
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
    
    def __convert_to_destination_table_format(self, table_id, destination_data_dict):
        # 比對 JSON 資料與 schema，填充缺失的欄位
        bq_created_time = datetime.now()
        bq_created_time_str = bq_created_time.strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        bq_updated_time_str = bq_created_time.strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        destination_data_dict["BQ_CREATED_TIME"]: bq_created_time_str
        destination_data_dict["BQ_UPDATED_TIME"]: bq_updated_time_str
        schema_field_names = self.__get_table_schema(table_id)
        filled_data = []
        for record in destination_data_dict:
            filled_record = {field: record.get(field, "") for field in schema_field_names}
            filled_data.append(filled_record)
        return filled_data

    def __convert_to_tmp_table_format(self, general_tmp_data_entity):
        """
        把 destination_data_dict 轉換成可以存入tmp表的格式

        Args:
            destination_data_dict (dict)

        Returns:
            dict: 可存入tmp表的格式
        """
        # 將 datetime 對象轉換為 RFC 3339 格式的字符串
        bq_created_time = datetime.now()
        bq_created_time_utc = bq_created_time.replace(tzinfo=timezone.utc)
        bq_created_time_str = bq_created_time_utc.isoformat()
        bq_created_time_str = bq_created_time.strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        bq_updated_time_str = bq_created_time.strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        general_tmp_data_entity.BQ_CREATED_TIME = bq_created_time_str
        general_tmp_data_entity.BQ_UPDATED_TIME = bq_updated_time_str

        # 把class轉dict
        bq_dict = vars(general_tmp_data_entity)
        print("DIC1", bq_dict)
        return bq_dict