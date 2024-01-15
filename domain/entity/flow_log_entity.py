class FlowLog:
    def __init__(
        self,
        DATETIME: str = "",
        FLOW_ID: str = "",
        FLOW_NAME: str = "",
        TASK_CODE: str = "",
        TASK_NAME: str = "",
        STATUS: str = "",
        MESSAGE: str = "",
        SEVERITY: str = ""
    ):
        """
        定義 FlowTaskData 實體的參數。

        Args:
            DATETIME (str): 記錄的時間戳。
            FLOW_ID (str): job的唯一識別碼。
            FLOW_NAME (str): job名稱。
            TASK_CODE (str): task代碼。
            TASK_NAME (str): task名稱。
            STATUS (str): 狀態，例如 Success 或 Error。
            MESSAGE (str): 錯誤信息。
            SEVERITY (str): 嚴重程度。
        """
        self.DATETIME = DATETIME
        self.FLOW_ID = FLOW_ID
        self.FLOW_NAME = FLOW_NAME
        self.TASK_CODE = TASK_CODE
        self.TASK_NAME = TASK_NAME
        self.STATUS = STATUS
        self.MESSAGE = MESSAGE
        self.SEVERITY = SEVERITY
