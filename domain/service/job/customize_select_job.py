import json
from datetime import datetime

from domain.domain_infra_port import DomainInfraPort
from domain.entity.general_tmp_data_entity import GeneralTmpData
from domain.service.job.job import Job


class CustomizeSelect(Job):
    def __init__(
        self, mission_id, mission_name, domain_infra_repository=DomainInfraPort()
    ):
        self.mission_id = mission_id
        self.mission_name = mission_name
        self.infra_repository = domain_infra_repository

    def execute(self, order_data, source_table_path, previous_job_id):
        """
        客製化查詢

        Args:
            source_table_path (_type_): 來源 table 路徑
            conditions (_type_, optional): 篩選條件

        Returns:
            list: 回傳資料
        """
        conditions = []
        try:
            conditions_list = order_data["select_conditions"]
            for condition in conditions_list:
                conditions.append(condition.format(**locals()))
            result_data_list = self.infra_repository.customize_select_from_source_table(
                source_table_path=source_table_path, conditions=conditions
            )
        except:
            result_data_list = self.infra_repository.customize_select_from_source_table(
                source_table_path=source_table_path
            )
        convert_data_list = []
        for result_data in result_data_list:
            convert_data_list.append(self.__convert_all_to_str(result_data))
        convert_data_list_json = json.dumps(convert_data_list)
        general_tmp_data_entity = GeneralTmpData(TMP_DATA=convert_data_list_json)
        print("list", convert_data_list_json)
        print("CustomizeSelect.entity", general_tmp_data_entity.TMP_DATA)
        return general_tmp_data_entity, ""

    def __convert_all_to_str(self, data):
        if isinstance(data, dict):
            return {k: self.__convert_all_to_str(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.__convert_all_to_str(v) for v in data]
        else:
            return str(data)
