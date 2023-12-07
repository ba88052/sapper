from domain.service.task.task import Task
from domain.domain_infra_port import DomainInfraPort
from domain.service.general_tmp_domain_service import GeneralTmpDataDomainService
from datetime import datetime
import json


class CustomizeSelect(Task):
    def __init__(self, mission_id, mission_name, domain_infra_respository=DomainInfraPort()):
        self.mission_id = mission_id
        self.mission_name = mission_name
        self.infra_respository = domain_infra_respository

    def execute(self, order_data, source_table_path, previous_task_id):
        """
        客製化查詢

        Args:
            source_table_path (_type_): 來源 table 路徑
            conditions (_type_, optional): 篩選條件

        Returns:
            list: 回傳資料
        """
        conditions = order_data["select_conditions"]
        result_data_list =  self.infra_respository.customize_select_from_source_table(source_table_path = source_table_path, 
                                                                                 conditions = conditions)
        result_data_list = json.dumps(str(result_data_list))
        general_tmp_data_entity = GeneralTmpDataDomainService().get_gemeral_tmp_data(
            TMP_DATA = result_data_list
        )
        print ("list", result_data_list)
        print("entity", general_tmp_data_entity.TMP_DATA)
        return general_tmp_data_entity
