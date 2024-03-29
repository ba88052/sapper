import json
from datetime import datetime, timezone

from infrastructure.bigquery.client.bq_client import BqClient
from infrastructure.config_handler import INFRA_CONFIG


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
        把 general_tmp_data_entity 存到bq

        Args:
            general_tmp_data_entity (general_tmp_data_entity實體)
            use_tmp_table(Booling):是否使用暫存表，使用表示還有下一個動作
        """
        print("use_tmp_table", use_tmp_table)
        if use_tmp_table == True:
            general_tmp_data_dict = self.__convert_to_tmp_table_format(
                general_tmp_data_entity
            )
            insertion_errors = self.client.insert_rows_json(
                self.bigquery_table_id, [general_tmp_data_dict]
            )
            if insertion_errors:
                print(
                    f"Errors occurred while storing destination_data_dict to BigQuery: {insertion_errors}"
                )
            else:
                print("destination_data_dict stored successfully to BigQuery.")
        else:
            for destination_data in general_tmp_data_entity.TMP_DATA:
                print("destination_data", destination_data)
                print("destination_data_type", type(destination_data))
                destination_data_dict = self.__convert_to_destination_table_format(
                    table_id=self.bigquery_table_id, destination_data=destination_data
                )
                insertion_errors = self.client.insert_rows_json(
                    self.bigquery_table_id, [destination_data_dict]
                )

                if insertion_errors:
                    print(
                        f"Errors occurred while storing destination_data_dict to BigQuery: {insertion_errors}"
                    )
                else:
                    print("destination_data_dict stored successfully to BigQuery.")

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

    def __convert_to_destination_table_format(self, table_id, destination_data):
        """
        # 比對 JSON 資料與 schema，填充缺失的欄位

        Args:
            table_id (str): 目標表的ID，或者說路徑
            destination_data (dict): 要儲存的data

        Returns:
            dict: 整理後的資料
        """

        bq_created_time = datetime.now()
        bq_created_time_str = bq_created_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
        bq_updated_time_str = bq_created_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
        partition_date = bq_created_time.strftime("%Y-%m-%d")
        destination_data["BQ_CREATED_TIME"] = bq_created_time_str
        destination_data["BQ_UPDATED_TIME"] = bq_updated_time_str
        destination_data["PARTITION_DATE"] = partition_date
        schema_field_names = self.__get_table_schema(table_id)
        filled_data = {}
        for field in schema_field_names:
            # 如果該欄位在 destination_data 中存在，則使用其值，否則使用預設值 ""
            filled_data[field] = destination_data.get(field, "")
        print(filled_data)
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
        bq_created_time_str = bq_created_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
        bq_updated_time_str = bq_created_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
        partition_date = bq_created_time.strftime("%Y-%m-%d")
        general_tmp_data_entity.BQ_CREATED_TIME = bq_created_time_str
        general_tmp_data_entity.BQ_UPDATED_TIME = bq_updated_time_str
        general_tmp_data_entity.PARTITION_DATE = partition_date
        # 把class轉dict
        bq_dict = vars(general_tmp_data_entity)
        return bq_dict
