from domain.entity.flow_log_entity import FlowLog
from domain.domain_infra_port import get_monitoring_config
import traceback
from flask import g

# 用 g. 來控制 flow_name flow_id 這類變數
# 要寫json來從task_name控制task_code
# 還有要吃task_name對應的severity
# 要跟他們用的同一個flow_log格式

class ErrorHandling:
    
    def __init__(self, flow_name):
        self.flow_name = flow_name
        self.monitoring_config = get_monitoring_config()
        self.save_flow_log = ""

    def error_handling_decorator(func):
        def wrapper(self, *args, **kwargs):
            flow_id = g.REQUEST_MESSAGE.JOB_ID
            flow_name = g.REQUEST_MESSAGE.JOB_NAME
            flow_log_entity = FlowLog(
                    DATETIME = "",
                    FLOW_ID = flow_id,
                    FLOW_NAME = flow_name,
                    TASK_CODE = "",
                    TASK_NAME = task_name,
                    STATUS = "",
                    MESSAGE = "",
                    SEVERITY = ""
                )
            try:
                result = func(self, *args, **kwargs)
                task_name = func.__name__
                flow_log_entity.STATUS = "Success"
                self.save_flow_log(flow_log_entity)
                return result
            except DebugError as d:
                error_info = str(d) + traceback.format_exc()
                error_info = error_info.replace("\n", "")
                flow_log_entity.STATUS = "Fail"
                flow_log_entity.SEVERITY = "DEBUG"
                flow_log_entity.MESSAGE = error_info
                self.save_flow_log(flow_log_entity)
                return result
            except Exception as e:
                error_info = str(e) + traceback.format_exc()
                error_info = error_info.replace("\n", "")
                flow_log_entity.STATUS = "Fail"
                flow_log_entity.SEVERITY = "ERROR"
                flow_log_entity.MESSAGE = error_info
                self.save_flow_log(flow_log_entity)
                raise
        return wrapper
    

class DebugError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)