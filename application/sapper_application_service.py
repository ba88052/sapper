from application.application_infra_port import ApplicationInfraPort
from domain.domain_infra_port import DomainInfraPort
from domain.service.job_selector import JobSelectorDomainService
from domain.entity.request_message_entity import RequestMessage
from domain.service.error_handling import FlowErrorHandler
import traceback
from flask import g

class SapperApplicationService:
    def __init__(self, message, application_infra_respository=ApplicationInfraPort(), domain_infra_respository=DomainInfraPort()):
        """
        初始化 SapperApplicationService 類。

        Args:
            message (dict): 包含工作流程所需信息的字典。
            application_infra_respository (ApplicationInfraPort): 應用程式基礎設施儲存庫。
            domain_infra_respository (DomainInfraPort): 領域基礎設施儲存庫。
        """
        # 解析消息並創建 RequestMessage 實體
        self.request_message_entity = RequestMessage(
            # ... 其他字段
        )
        # 初始化其他屬性
        self.report_message = message
        self.report_message["job_status"] = "Process"
        self.report_message["note"] = ""
        self.application_infra_respository = application_infra_respository
        self.domain_infra_respository = domain_infra_respository
        self.job_selector = JobSelectorDomainService()

    def execute(self):
        """
        根據傳入的job_name和order_data執行子任務
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
def select_job(self):
    """
    選擇要執行的工作。
    
    根據請求訊息實體中的工作名稱(JOB_NAME)、任務ID(MISSION_ID)和任務名稱(MISSION_NAME)
    從工作選擇器(job_selector)中選擇合適的工作。
    
    Returns:
        Object: 選擇的工作對象。
    """
    job = self.job_selector.select(
        job_name=self.request_message_entity.JOB_NAME,
        mission_id=self.request_message_entity.MISSION_ID,
        mission_name=self.request_message_entity.MISSION_NAME,
        domain_infra_respository=self.domain_infra_respository
    )
    return job

def run_job(self, job):
    """
    執行選擇的工作。
    
    傳遞訂單數據(ORDER_DATA)、源表路徑(SOURCE_TABLE_PATH)和先前工作ID(PREVIOUS_JOB_ID)
    給選擇的工作並執行該工作。
    
    Args:
        job (Object): 待執行的工作對象。
    
    Returns:
        Object: 執行工作後生成的臨時數據實體。
    """
    general_tmp_data_entity = job.execute(
        order_data=self.request_message_entity.ORDER_DATA,
        source_table_path=self.request_message_entity.SOURCE_TABLE_PATH,
        previous_job_id=self.request_message_entity.PREVIOUS_JOB_ID
    )
    print(general_tmp_data_entity.TMP_DATA)
    return general_tmp_data_entity

def add_shared_data(self, general_tmp_data_entity):
    """
    為臨時數據實體添加共用數據。
    
    將請求訊息實體中的任務ID(MISSION_ID)、任務名稱(MISSION_NAME)、
    工作名稱(JOB_NAME)和工作ID(JOB_ID)添加到臨時數據實體中。
    
    Args:
        general_tmp_data_entity (Object): 臨時數據實體。
    """
    general_tmp_data_entity.UUID_Request = self.request_message_entity.MISSION_ID
    general_tmp_data_entity.MISSION_NAME = self.request_message_entity.MISSION_NAME
    general_tmp_data_entity.JOB_NAME = self.request_message_entity.JOB_NAME
    general_tmp_data_entity.JOB_ID = self.request_message_entity.JOB_ID

def save_data(self, general_tmp_data_entity):
    """
    將臨時數據保存到數據庫。
    
    將臨時數據實體存儲到目標表路徑(DESTINATION_TABLE_PATH)並更新報告消息的狀態。
    
    Args:
        general_tmp_data_entity (Object): 臨時數據實體。
    """
    self.application_infra_respository.save_general_tmp_data(
        destination_table_path=self.request_message_entity.DESTINATION_TABLE_PATH,
        general_tmp_data_entity=general_tmp_data_entity,
        use_tmp_table=self.request_message_entity.USE_GENERAL_TMP_TABLE
    )
    self.report_message["job_status"] = "Success"

def report_job(self):
    """
    回報工作完成狀態。
    
    將工作完成的狀態和其他相關信息傳遞給應用程式基礎設施儲存庫以進行記錄和後續處理。
    """
    print(
        self.application_infra_respository.report_job_completed(
            report_return_path=self.request_message_entity.REPORT_PATH,
            report_message=self.report_message
        )
    )
