import json
from google.cloud import logging

from domain.domain_infra_port import DomainInfraPort
from infrastructure.bigquery.repository.flow_log_respository import \
    FLowLogRepository
from infrastructure.bigquery.repository.source_table_repository import \
    SourceTableRepository
from infrastructure.config_handler import INFRA_CONFIG, MONITORING_CONFIG


class DomainRespositoryAdapter(DomainInfraPort):
    def __init__(self):
        self.config_file = "config.json"

    def get_infra_config(self):
        """
        讀取 infra 參數檔
        """
        return INFRA_CONFIG

    def get_monitoring_config(self):
        """
        讀取 monitoring 參數檔
        """
        return MONITORING_CONFIG

    def customize_select_from_source_table(self, source_table_path, conditions):
        """
        客製化查詢source_table

        Args:
            source_table_path (_type_): _description_
            conditions (_type_): _description_
        """
        result_data = SourceTableRepository(
            source_table_path=source_table_path
        ).customize_select(conditions=conditions)
        return result_data

    def get_general_tmp_table_data(self, source_table_path, previous_job_id):
        """
        獲取 tmp_table 的 data

        Args:
            source_table_path (_type_): _description_
        """
        result_data = SourceTableRepository(
            source_table_path=source_table_path
        ).customize_select(conditions=[f"JOB_ID = '{previous_job_id}'"])
        return result_data

    def save_flow_log(self, flow_log_entity):
        """
        存 flow_log ，還需要發送 logging 到對應服務中做紀錄
        """
        FLowLogRepository().save(flow_log_entity)
        logging_client = logging.Client()
        log_name = "custom-log"
        logger = logging_client.logger(log_name)
        flow_log_dict = vars(flow_log_entity)
        severity=flow_log_entity.SEVERITY
        # 在發log時沒有NOTICE這個層級，但組內有制定NOTICE層級，所以轉成DEBUG出去，這是一個有點蠢的動作。
        if severity == "NOTICE":
            severity= "DEBUG"
        logger.log_struct(flow_log_dict, severity=flow_log_entity.SEVERITY)
