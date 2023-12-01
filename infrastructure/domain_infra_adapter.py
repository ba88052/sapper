from domain.domain_infra_port import DomainInfraPort
from infrastructure.infra_config_handler import CONFIG
import json
from infrastructure.bigquery.repository.api_log_repository import ApiLogRepository



class DomainRespositoryAdapter(DomainInfraPort):
    def __init__(self):
        self.config_file = "config.json"

    def save_api_log_entity_list(self, api_log_entity_list):
        """把實體化後的Entity資料，存入DB

        Args:
            api_log_entity_list (list): 參照api_log_entity
        """
        for api_log in api_log_entity_list:
            ApiLogRepository().save(api_log=api_log)
            
        

    def get_config(self):
        """
        讀取參數檔
        """
        return CONFIG