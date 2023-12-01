from datetime import datetime

class GeneralTempTable:
    def __init__(
        self,
        UUID_Request: str = "",
        MISSION_NAME: str = "",
        TASK_ID : str = "",
        TASK_NAME: str = "",
        TEMP_DATA: str = "",
        TASK_SEQUENCE: str = "",
        BQ_CREATED_TIME: datetime = datetime.now(),
        BQ_UPDATED_TIME: datetime = datetime.now()
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
        self.TEMP_DATA = TEMP_DATA
        self.TASK_SEQUENCE = TASK_SEQUENCE
        self.BQ_CREATED_TIME = BQ_CREATED_TIME if BQ_CREATED_TIME else datetime.now()
        self.BQ_UPDATED_TIME = BQ_UPDATED_TIME if BQ_UPDATED_TIME else datetime.now()
