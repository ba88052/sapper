from domain.entity.flow_log_entity import FlowLog
from domain.domain_infra_port import DomainInfraPort
from flask import g
import traceback
from datetime import datetime

# 需要在被裝飾的函數中有包含 self.request_message_entity 和 self.domain_infra_respository

class FlowErrorHandler:
    @classmethod
    def flow_log_decorator(cls, func):
        """
        用於記錄流程日誌的裝飾器。
        Args:
            func (function): 被裝飾的函數。
        Returns:
            function: 包裝後的函數。
        """
        # 包裝函數
        def wrapper(service_instance, *args, **kwargs):
            # 設置流程相關的屬性
            cls.flow_id = f"{service_instance.job_name}_{service_instance.mission_id}_{service_instance.job_id}"
            cls.flow_name = f"{service_instance.mission_name}_{service_instance.job_name}"
            cls.executor = service_instance.executor
            cls.infra_respository = service_instance.domain_infra_respository
            cls.monitoring_config = cls.infra_respository.get_monitoring_config()
            
            # 記錄當前時間
            current_time = datetime.now()
            current_time_str = current_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            task_name = func.__name__
            flow_log_entity = FlowLog(DATETIME = current_time_str, FLOW_ID = cls.flow_id, FLOW_NAME = cls.flow_name, TASK_NAME = task_name)
            try:
                # 執行被裝飾的函數
                result = func(service_instance, *args, **kwargs)
                # 記錄成功日誌
                cls.flow_log_on_success(log_entity = flow_log_entity)
                return result
            except DebugError as d:
                # 記錄不影響流程的錯誤日誌
                cls.flow_log_on_fail(log_entity = flow_log_entity, error = d, severity = "DEBUG")
                return
            except Exception as e:
                # 記錄一般錯誤日誌
                cls.flow_log_on_fail(log_entity = flow_log_entity, error = e, severity = "ERROR")
                raise
        return wrapper

    @classmethod
    def flow_log_on_success(cls, log_entity):
        """
        處理日誌記錄成功的情況。
        Args:
            log_entity (FlowLog): 日誌實體。
        """
        log_entity.STATUS = "Success"
        log_entity.SEVERITY = "INFO"
        log_entity.TASK_CODE = cls.task_code_maker(executor = cls.executor, task_name = log_entity.TASK_NAME, severity = log_entity.SEVERITY)
        cls.infra_respository.save_flow_log(log_entity)

    @classmethod
    def flow_log_on_fail(cls, log_entity, error, severity):
        """
        處理日誌記錄失敗的情況。
        Args:
            log_entity (FlowLog): 日誌實體。
            error (Exception): 發生的錯誤。
            severity (str): 錯誤嚴重性。
        """
        error_info = str(error) + traceback.format_exc()
        log_entity.STATUS = "Fail"
        log_entity.SEVERITY = severity
        log_entity.MESSAGE = error_info.replace("\n", "")
        log_entity.TASK_CODE = cls.task_code_maker(executor = cls.executor, task_name = log_entity.TASK_NAME, severity = log_entity.SEVERITY)
        cls.infra_respository.save_flow_log(log_entity)
    
    @classmethod
    def task_code_maker(cls, executor, task_name, severity):
        """
        生成任務代碼。
        Args:
            executor (str): 執行者。
            task_name (str): 任務名稱。
            severity (str): 嚴重性級別。
        Returns:
            str: 任務代碼。
        """
        flow_number = cls.monitoring_config["flow_mapping"][executor]
        task_number = cls.monitoring_config["task_mapping"][executor][task_name]
        severity_number = cls.monitoring_config["severity_mapping"][severity]
        task_code = flow_number + task_number + severity_number
        return task_code


class DebugError(Exception):
    """ 自定義的不影響流程的錯誤類別。"""

    def __init__(self, message):
        """
        初始化錯誤。
        Args:
            message (str): 錯誤信息。
        """
        self.message = message
        super().__init__(self.message)
