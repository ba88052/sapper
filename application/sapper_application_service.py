from application.application_infra_port import ApplicationInfraPort
from domain.domain_infra_port import DomainInfraPort
from domain.service.job_selector import JobSelectorDomainService
from domain.entity.request_message_entity import RequestMessage
from domain.service.error_handling import FlowErrorHandler
import traceback
from flask import g


class SapperApplicationService:
    def __init__(self, message, application_infra_respository=ApplicationInfraPort(), domain_infra_respository=DomainInfraPort()):
        """_summary_

        Args:
            message (dict)
            application_infra_respository (_type_): _description_
        """
        self.request_message_entity = RequestMessage(
            ORDER_DATA=message["order_data"],
            MISSION_NAME=message["mission_name"],
            MISSION_ID=message["mission_id"],
            PREVIOUS_JOB_ID=message["previous_job_id"],
            JOB_ID=message["job_id"],
            JOB_NAME=message["job_name"],
            JOB_SEQUENCE=message["job_sequence"],
            REPORT_PATH=message["job_report_path"],
            SOURCE_TABLE_PATH=message["source_table_path"],
            DESTINATION_TABLE_PATH=message["destination_table_path"],
            JOB_STATUS=message["job_status"],
            USE_GENERAL_TMP_TABLE=message["use_general_tmp_table"],
        )
        # self.flow_error_handler = FlowErrorHandler(flow_name = self.request_message_entity.JOB_NAME,
        #                                             flow_id = self.request_message_entity.JOB_ID,
        #                                             executor = self.executor, 
        #                                             domain_infra_respository = application_infra_respository)
        self.report_message = message
        self.report_message["job_status"] = "Process"
        self.report_message["note"] = ""
        self.application_infra_respository = application_infra_respository
        self.domain_infra_respository = domain_infra_respository
        self.job_selector = JobSelectorDomainService()

    def execute(self):
        """
        根據傳入的job_name，和order_data執行子任務
        """
        #  Task 1
        #  根據 job_name 選擇子任務 job
        job = self.select_job()

        # Task 2
        # 將 order_data 丟入 job 中執行任務
        general_tmp_data_entity = self.run_job(job)

        # Task 3
        # 加入一些通用資料
        self.add_shared_data(general_tmp_data_entity = general_tmp_data_entity)

        # Task 4
        # 存入資料庫
        self.save_data(general_tmp_data_entity = general_tmp_data_entity)
        self.report_message["job_status"] = "Success"
        
        # Task 5
        # 回報任務狀態
        self.report_job()

    
    @FlowErrorHandler.flow_log_decorator
    def select_job(self):
        job = self.job_selector.select(
            job_name=self.request_message_entity.JOB_NAME,
            mission_id=self.request_message_entity.MISSION_ID,
            mission_name=self.request_message_entity.MISSION_NAME,
            domain_infra_respository=self.domain_infra_respository
            )
        return job
    
    @FlowErrorHandler.flow_log_decorator
    def run_job(self, job):
        general_tmp_data_entity = job.execute(
                order_data=self.request_message_entity.ORDER_DATA,
                source_table_path=self.request_message_entity.SOURCE_TABLE_PATH,
                previous_job_id=self.request_message_entity.PREVIOUS_JOB_ID
            )
        print(general_tmp_data_entity.TMP_DATA)
        return general_tmp_data_entity

    @FlowErrorHandler.flow_log_decorator
    def add_shared_data(self, general_tmp_data_entity):
        general_tmp_data_entity.UUID_Request = self.request_message_entity.MISSION_ID
        general_tmp_data_entity.MISSION_NAME = self.request_message_entity.MISSION_NAME
        general_tmp_data_entity.JOB_NAME = self.request_message_entity.JOB_NAME
        general_tmp_data_entity.JOB_ID = self.request_message_entity.JOB_ID

    @FlowErrorHandler.flow_log_decorator
    def save_data(self, general_tmp_data_entity):
        self.application_infra_respository.save_general_tmp_data(
            destination_table_path=self.request_message_entity.DESTINATION_TABLE_PATH,
            general_tmp_data_entity=general_tmp_data_entity,
            use_tmp_table=self.request_message_entity.USE_GENERAL_TMP_TABLE
        )
        self.report_message["job_status"] = "Success"

    @FlowErrorHandler.flow_log_decorator
    def report_job(self):
        print(
            self.application_infra_respository.report_job_completed(
                report_return_path=self.request_message_entity.REPORT_PATH,
                report_message=self.report_message
            )
        )