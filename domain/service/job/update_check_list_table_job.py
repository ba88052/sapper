import json
from datetime import datetime

from domain.domain_infra_port import DomainInfraPort
from domain.entity.general_tmp_data_entity import GeneralTmpData
from domain.service.job.job import Job


class UpdateCheckListTableJob(Job):
    def __init__(
        self, mission_id, mission_name, domain_infra_repository=DomainInfraPort()
    ):
        self.mission_id = mission_id
        self.mission_name = mission_name
        self.infra_repository = domain_infra_repository

    def execute(self, order_data, source_table_path, previous_job_id):
        """
        table已完成更新，接著要讓 check_list 表格的狀態改為1

        Args:
            source_table_path (str): 完成更新的table

        Returns:
            GeneralTmpData: 包含更新資料的實體
        """
        # 解析 dataset_name 和 table_name
        dataset_name, table_name = source_table_path.split('.')
        current_time = datetime.now().isoformat()
        
        # 準備更新到 check_list 表的資料
        update_data = {
            "BQ_UPDATED_TIME": current_time,
            "DATASET": dataset_name,
            "TABLE": table_name,
            "UPDATE_STATUS": 1
        }

        # 轉換更新資料為JSON格式並封裝到GeneralTmpData中
        update_data_json = json.dumps(update_data)
        general_tmp_data_entity = GeneralTmpData(TMP_DATA=update_data_json)
        print("UpdateCheckListTableJob.entity", general_tmp_data_entity.TMP_DATA)
        return general_tmp_data_entity
