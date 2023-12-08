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
        convert_data_list = []
        for result_data in result_data_list:
            convert_data_list.append(self.__convert_all_to_str(result_data))
        convert_data_list_json = json.dumps(convert_data_list)
        general_tmp_data_entity = GeneralTmpDataDomainService().get_gemeral_tmp_data(
            TMP_DATA = convert_data_list_json
        )
        print ("list", convert_data_list_json)
        print("entity", general_tmp_data_entity.TMP_DATA)
        return general_tmp_data_entity
    
    def __convert_all_to_str(self, data): 
        if isinstance(data, dict):
                return {k: self.convert_all_to_str(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.convert_all_to_str(v) for v in data]
        else:
            return str(data)

