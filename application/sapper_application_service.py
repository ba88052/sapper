from application.application_infra_port import ApplicationInfraPort
from domain.service.job_selector import JobSelectorDomainService
from domain.entity.request_message_entity import RequestMessage
import traceback
from flask import g


class SapperApplicaionService:
    def __init__(self, message, application_infra_respository=ApplicationInfraPort()):
        """_summary_

        Args:
            order_dict (dict): 內部要有parent_job_id, job_name
            db_respository (_type_): _description_
        """
        self.request_message = RequestMessage(
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
        self.report_message = message
        self.report_message["job_status"] = "Process"
        self.report_message["note"] = ""
        self.application_infra_respository = application_infra_respository
        self.job_selector = JobSelectorDomainService()

    def execute_job(self):
        """
        根據傳入的job_name，和order_data執行子任務
        """
        try:
            #  Task 1
            #  根據 job_name 選擇子任務 job
            job = self.job_selector.select(
                job_name=self.request_message.JOB_NAME,
                mission_id=self.request_message.MISSION_ID,
                mission_name=self.request_message.MISSION_NAME,
                domain_infra_respository=g.DOMAIN_INFRA_ADAPTER
            )

            # Task 2
            # 將 order_data 丟入 job 中執行任務
            general_tmp_data_entity = job.execute(
                order_data=self.request_message.ORDER_DATA,
                source_table_path=self.request_message.SOURCE_TABLE_PATH,
                previous_job_id=self.request_message.PREVIOUS_JOB_ID
            )
            print(general_tmp_data_entity.TMP_DATA)

            # Task 3
            # 加入一些通用資料
            general_tmp_data_entity.UUID_Request = self.request_message.MISSION_ID
            general_tmp_data_entity.MISSION_NAME = self.request_message.MISSION_NAME
            general_tmp_data_entity.JOB_NAME = self.request_message.JOB_NAME
            general_tmp_data_entity.JOB_ID = self.request_message.JOB_ID

            # Task 4
            # 存入資料庫
            self.application_infra_respository.save_general_tmp_data(
                destination_table_path=self.request_message.DESTINATION_TABLE_PATH,
                general_tmp_data_entity=general_tmp_data_entity,
                use_tmp_table=self.request_message.USE_GENERAL_TMP_TABLE
            )
            self.report_message["job_status"] = "Success"

        except Exception as e:
            error_info = str(e) + traceback.format_exc()
            error_info = error_info.replace("\n", "")
            print("ERROR_INFO:", error_info)
            self.report_message["job_status"] = "Fail"
            self.report_message["note"] = error_info

        # Task 5
        # 回報任務狀態
        print(
            self.application_infra_respository.report_job_completed(
                report_return_path=self.request_message.REPORT_PATH,
                report_message=self.report_message
            )
        )
