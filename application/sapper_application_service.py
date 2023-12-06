from application.application_infra_port import \
    ApplicationInfraPort
from domain.service.task_selector import TaskSelectorDomainService
from domain.service.request_message_domain_service import RequestMessageDomainService
import traceback
from flask import g


class SapperApplicaionService:
    def __init__(self, message, application_infra_respository=ApplicationInfraPort()):
        """_summary_

        Args:
            order_dict (dict): 內部要有parent_job_id, job_name
            db_respository (_type_): _description_
        """
        self.request_message = RequestMessageDomainService().get_request_message(
            ORDER_DATA = message["order_data"],
            MISSION_NAME = message["mission_name"],
            MISSION_ID = message["mission_id"],
            PREVIOUS_TASK_ID = message["previous_task_id"],
            TASK_ID = message["task_id"],
            TASK_NAME = message["task_name"],
            TASK_SEQUENCE = message["task_sequence"],
            REPORT_PATH = message["report_path"],
            SOURCE_TABLE_PATH = message["source_table_path"],
            DESTINATION_TABLE_PATH = message["destination_table_path"],
            TASK_STATUS = message["task_status"],
            USE_GENERAL_TMP_TABLE = message["use_general_tmp_table"],
        )
        self.report_message = message
        self.report_message["task_status"] = "Process"
        self.report_message["note"] = ""
        self.application_infra_respository = application_infra_respository
        self.task_selector = TaskSelectorDomainService()

    def execute_task(self):
        """
        根據傳入的task_name，和order_data執行子任務
        """
        try:
            # 根據 task_name 選擇子任務 task
            task = self.task_selector.select(
                task_name = self.request_message.TASK_NAME,
                mission_id = self.request_message.MISSION_ID,
                mission_name = self.request_message.MISSION_NAME,
                domain_infra_respository = g.DOMAIN_INFRA_ADAPTER
            )

            # 將 order_data 丟入 task 中執行任務
            general_tmp_data_entity = task.execute(order_data = self.request_message.ORDER_DATA,
                                                source_table_path = self.request_message.SOURCE_TABLE_PATH,
                                                previous_task_id = self.request_message.PREVIOUS_TASK_ID)
            print(general_tmp_data_entity.TMP_DATA)

            # 加入一些存table時需要的欄位
            general_tmp_data_entity.UUID_Request = self.request_message.MISSION_ID,
            general_tmp_data_entity.MISSION_NAME = self.request_message.MISSION_NAME
            general_tmp_data_entity.TASK_NAME = self.request_message.TASK_NAME
            general_tmp_data_entity.TASK_ID = self.request_message.TASK_ID

            self.application_infra_respository.save_general_tmp_data(
                                                            destination_table_path = self.request_message.DESTINATION_TABLE_PATH, 
                                                            general_tmp_data_entity = general_tmp_data_entity,
                                                            use_tmp_table = self.request_message.USE_GENERAL_TMP_TABLE)
            self.report_message["task_status"] = "Success"

        except Exception as e:
            error_info = str(e) + traceback.format_exc()
            error_info = error_info.replace("\n", "")
            print("ERROR_INFO:", error_info)
            self.report_message["task_status"] = "Fail"
            self.report_message["note"] = error_info

        # 回報任務狀態
        print(self.infra_respository.report_task_completed(report_return_path = self.report_path, 
                                                           report_message = self.report_message))
        

            
            
