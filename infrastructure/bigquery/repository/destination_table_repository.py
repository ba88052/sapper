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
        self.bigquery_table_id = destination_table_path
        self.table_schema = self.__get_table_schema(self.bigquery_table_id)

    def save(self, general_tmp_data_entity_list, use_tmp_table: bool):
        """
        把 general_tmp_data_entity 存到bq

        Args:
            general_tmp_data_entity_list (list): general_tmp_data_entity實體的列表
            use_tmp_table (bool): 是否使用暫存表，使用表示還有下一個動作
        """
        data_to_insert = []
        for general_tmp_data_entity in general_tmp_data_entity_list:
            if use_tmp_table:
                general_tmp_data_dict = self.__convert_to_tmp_table_format(general_tmp_data_entity)
                data_to_insert.append(general_tmp_data_dict)
            else:
                UUID_Request = general_tmp_data_entity.UUID_Request
                MISSION_NAME = general_tmp_data_entity.MISSION_NAME
                JOB_NAME = general_tmp_data_entity.JOB_NAME
                JOB_ID = general_tmp_data_entity.JOB_ID
                for destination_data in general_tmp_data_entity.TMP_DATA:
                    destination_data_dict = self.__convert_to_destination_table_format(destination_data, UUID_Request, MISSION_NAME, JOB_NAME, JOB_ID)
                    data_to_insert.append(destination_data_dict)

        insertion_errors = self.client.insert_rows_json(self.bigquery_table_id, data_to_insert)
        if insertion_errors:
            print(f"Errors occurred while storing data to BigQuery: {insertion_errors}")
        else:
            print("Data stored successfully to BigQuery.")

    def __get_table_schema(self, table_id):
        """
        獲取 BigQuery 表的 schema

        Args:
            table_id (str): 目標表的ID，或者說路徑

        Returns:
            dict: 目標表的schema dict
        """
        table = self.client.get_table(table_id)
        schema_field_names = {field.name for field in table.schema}
        return schema_field_names

    def __convert_to_destination_table_format(self, destination_data, UUID_Request, MISSION_NAME, JOB_NAME, JOB_ID):
        """
        比對 JSON 資料與 schema，填充缺失的欄位

        Args:
            destination_data (dict): 要儲存的data
            UUID_Request (str): 任務ID
            MISSION_NAME (str): 任務名稱
            JOB_NAME (str): 工作名稱
            JOB_ID (str): 工作ID

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
        destination_data["UUID_Request"] = UUID_Request
        destination_data["MISSION_NAME"] = MISSION_NAME
        destination_data["JOB_NAME"] = JOB_NAME
        destination_data["JOB_ID"] = JOB_ID

        filled_data = {field: destination_data.get(field, "") for field in self.table_schema}
        return filled_data

    def __convert_to_tmp_table_format(self, general_tmp_data_entity):
        """
        把 general_tmp_data_entity 轉換成可以存入tmp表的格式

        Args:
            general_tmp_data_entity: general_tmp_data_entity 實體

        Returns:
            dict: 可存入tmp表的格式
        """
        bq_created_time = datetime.now()
        bq_created_time_utc = bq_created_time.replace(tzinfo=timezone.utc)
        bq_created_time_str = bq_created_time_utc.isoformat()
        bq_updated_time_str = bq_created_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
        partition_date = bq_created_time.strftime("%Y-%m-%d")

        general_tmp_data_entity.BQ_CREATED_TIME = bq_created_time_str
        general_tmp_data_entity.BQ_UPDATED_TIME = bq_updated_time_str
        general_tmp_data_entity.PARTITION_DATE = partition_date

        bq_dict = vars(general_tmp_data_entity)
        return bq_dict
