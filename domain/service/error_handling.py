from domain.entity.flow_log_entity import FlowLog
from domain.domain_infra_port import DomainInfraPort
from flask import g
import traceback
from datetime import datetime

class FlowErrorHandler:
    @classmethod
    def flow_log_decorator(cls, func):
        """ 流程日誌裝飾器，用於記錄任務的成功或失敗狀態。

        Args:
            func (function): 被裝飾的函數。

        Returns:
            function: 包裝後的函數。

        """
        def wrapper(service_instance, *args, **kwargs):
            cls.flow_name = service_instance.request_message_entity.JOB_NAME
            print("裝飾器 flow name", cls.flow_name)
            cls.flow_id = service_instance.request_message_entity.JOB_ID
            print("裝飾器 flow id", cls.flow_id)
            cls.executor = g.EXECUTOR
            cls.infra_respository = service_instance.domain_infra_respository
            cls.monitoring_config = cls.infra_respository.get_monitoring_config()
            
            current_time = datetime.now()
            current_time_str = current_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            task_name = func.__name__
            flow_log_entity = FlowLog(DATETIME = current_time_str, FLOW_ID = cls.flow_id, FLOW_NAME = cls.flow_name, TASK_NAME = task_name)
            try:
                result = func(cls, *args, **kwargs)
                cls.flow_log_on_success(log_entity = flow_log_entity, task_name = task_name)
                return result
            except DebugError as d:
                cls.flow_log_on_fail(log_entity = flow_log_entity, error = d, severity = "DEBUG")
                return
            except Exception as e:
                cls.flow_log_on_fail(log_entity = flow_log_entity, error = e, severity = "ERROR")
                raise
        return wrapper

    @classmethod
    def flow_log_on_success(cls, log_entity):
        """ 當任務成功時記錄流程日誌。

        Args:
            log_entity (FlowLog): 流程日誌實體。

        """
        log_entity.STATUS = "Success"
        log_entity.SEVERITY = "INFO"
        log_entity.TASK_CODE = cls.task_code_maker(executor = cls.executor, task_name = log_entity.TASK_NAME, severity = log_entity.SEVERITY)
        cls.infra_respository.save_flow_log(log_entity)

    @classmethod
    def flow_log_on_fail(cls, log_entity, error, severity):
        """ 當任務失敗時記錄流程日誌。

        Args:
            log_entity (FlowLog): 流程日誌實體。
            error (Exception): 錯誤信息。
            severity (str): 錯誤嚴重程度。

        """
        error_info = str(error) + traceback.format_exc()
        log_entity.STATUS = "Fail"
        log_entity.SEVERITY = severity
        log_entity.MESSAGE = error_info.replace("\n", "")
        log_entity.TASK_CODE = cls.task_code_maker(executor = cls.executor, task_name = log_entity.TASK_NAME, severity = log_entity.SEVERITY)
        cls.infra_respository.save_flow_log(log_entity)
    
    @classmethod
    def task_code_maker(cls, executor, task_name, severity):
        """ 生成任務代碼。

        Args:
            executor (_type_): 執行者。
            task_name (str): 任務名稱。
            severity (str): 嚴重程度。

        Returns:
            str: 生成的任務代碼。

        """
        flow_number = cls.monitoring_config["flow_mapping"][executor]
        task_number = cls.monitoring_config["task_mapping"][executor][task_name]
        severity_number = cls.monitoring_config["severity_mapping"][severity]
        task_code = flow_number + task_number + severity_number
        return task_code


class DebugError(Exception):
    """ 自定義的調試錯誤類別。"""

    def __init__(self, message):
        """ 初始化調試錯誤。

        Args:
            message (str): 錯誤信息。

        """
        self.message = message
        super().__init__(self.message)
