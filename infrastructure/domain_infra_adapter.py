from domain.domain_infra_port import DomainInfraPort
from infrastructure.infra_config_handler import CONFIG
import json
from infrastructure.bigquery.repository.source_table_repository import SourceTableRepository



class DomainRespositoryAdapter(DomainInfraPort):
    def __init__(self):
        self.config_file = "config.json"  

    def get_config(self):
        """
        讀取參數檔
        """
        return CONFIG
    
    def customize_select_from_source_table(self, source_table_path, conditions):
        """
        客製化查詢source_table

        Args:
            source_table_path (_type_): _description_
            conditions (_type_): _description_
        """
        SourceTableRepository(source_table_path = source_table_path).customize_select(conditions = conditions)

    def get_general_tmp_table_data(self, source_table_path, previous_task_id):
        """
        獲取 tmp_table 的 data

        Args:
            source_table_path (_type_): _description_
        """
        SourceTableRepository(source_table_path = source_table_path).customize_select(conditions = f"TASK_ID = {previous_task_id}")
        