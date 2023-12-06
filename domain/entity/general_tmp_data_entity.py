from datetime import datetime

class GeneralTmpData:
    def __init__(
        self,
        UUID_Request: str = "",
        MISSION_NAME: str = "",
        TASK_ID : str = "",
        TASK_NAME: str = "",
        TMP_DATA: list = [],
        TASK_SEQUENCE: str = "",
        USE_GENERAL_TEMP_TABLE: str = "",
        BQ_CREATED_TIME: str = "",
        BQ_UPDATED_TIME: str = ""
    ):
        """
        定義 RawTable 實體的參數。

        Args:
            UUID_Request (str): Mission的唯一識別碼。
            MISSION_NAME (str): Mission的名稱。
            TASK_NAME (str): 子任務名稱。
            RAW_DATA (str): 原始數據。
            BQ_CREATED_TIME (datetime): 記錄創建時間。
            BQ_UPDATED_TIME (datetime): 記錄更新時間。
        """
        self.UUID_Request = UUID_Request
        self.MISSION_NAME = MISSION_NAME
        self.TASK_ID = TASK_ID
        self.TASK_NAME = TASK_NAME
        self.TMP_DATA = TMP_DATA
        self.TASK_SEQUENCE = TASK_SEQUENCE
        self.BQ_CREATED_TIME = BQ_CREATED_TIME 
        self.BQ_UPDATED_TIME = BQ_UPDATED_TIME 
        self.USE_GENERAL_TEMP_TABLE = USE_GENERAL_TEMP_TABLE
