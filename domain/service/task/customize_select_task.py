from domain.service.task.task import Task
from domain.domain_infra_port import DomainInfraPort
from datetime import datetime
import json


class CustomizeSelect(Task):
    def __init__(self, mission_id, mission_name, domain_infra_respository=DomainInfraPort()):
        self.mission_id = mission_id
        self.mission_name = mission_name
        self.infra_respository = domain_infra_respository
        self.config_file = self.infra_respository.get_config()["call_seon_fraud_api"]

    def execute(self, source_table_path, conditions=None):
        """
        客製化查詢

        Args:
            source_table_path (_type_): 來源 table 路徑
            conditions (_type_, optional): 篩選條件

        Returns:
            dict: 回傳資料
        """
        # 基本查詢
        query = f"SELECT * FROM `{source_table_path}`"

        # 添加條件
        if conditions:
            query += " WHERE " + " ".join(conditions)
        result_data =  self.infra_respository.run_query(query)
        return result_data
