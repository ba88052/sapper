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
        table_name = self.__remove_prefix(table_name, "TMP_")
        current_time = datetime.now().isoformat()
        
        # 準備更新到 check_list 表的資料
        update_data = {
            "BQ_UPDATED_TIME": current_time,
            "DATASET": dataset_name,
            "TABLE": table_name,
            "UPDATE_STATUS": 1
        }

        #只是for anamization 使用，用於刪除check_list_summary中的動作，不使用時請刪除這段有點醜的程式
        delete_sql = self.generate_delete_sql(dataset_name=dataset_name)
        self.infra_repository.run_query(delete_sql)

        # 轉換更新資料為JSON格式並封裝到GeneralTmpData中
        # update_data_json = json.dumps(update_data)
        update_data_json_list = [update_data]
        general_tmp_data_entity = GeneralTmpData(TMP_DATA=update_data_json_list)
        print("UpdateCheckListTableJob.entity", general_tmp_data_entity.TMP_DATA)
        return general_tmp_data_entity, ""

    def __remove_prefix(self, text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        return text  # 如果不是以指定的前綴開頭，則返回原文本
    

    #只是for anamization 使用，不使用時請刪除這段有點醜的程式
    def generate_delete_sql(self, dataset_name):
        """
        生成用於刪除符合特定條件記錄的 SQL 語句。

        參數:
            dataset_name (str): 需要匹配的 DATASET 值。
            table_name (str): 目標表名。

        返回:
            str: 生成的 SQL 語句。
        """
        # 獲取今天的日期，格式為 YYYY-MM-DD
        today_date = datetime.now().strftime("%Y-%m-%d")
        
        sql = f"""
        DELETE FROM `LOG_DATASET.OTHER_CHECKSUMMARY`
        WHERE BQ_DATE = '{today_date}'
        AND DATASET = '{dataset_name}'
        AND STATUS = '1'
        AND REMARK = '1'
        """
        
        return sql
