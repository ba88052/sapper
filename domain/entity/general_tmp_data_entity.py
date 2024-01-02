from datetime import datetime

# 優化方向 TMP DATA 改存 GCS or 改成 每一個只能處理單筆資料

class GeneralTmpData:
    def __init__(
        self,
        UUID_Request: str = "",
        MISSION_NAME: str = "",
        JOB_ID: str = "",
        JOB_NAME: str = "",
        TMP_DATA: list = [],
        JOB_SEQUENCE: str = "",
        BQ_CREATED_TIME: str = "",
        BQ_UPDATED_TIME: str = "",
    ):
        """
        定義 RawTable 實體的參數。

        Args:
            UUID_Request (str): Mission的唯一識別碼。
            MISSION_NAME (str): Mission的名稱。
            JOB_NAME (str): job名稱。
            RAW_DATA (str): 原始數據。
            BQ_CREATED_TIME (datetime): 記錄創建時間。
            BQ_UPDATED_TIME (datetime): 記錄更新時間。
        """
        self.UUID_Request = UUID_Request
        self.MISSION_NAME = MISSION_NAME
        self.JOB_ID = JOB_ID
        self.JOB_NAME = JOB_NAME
        self.TMP_DATA = TMP_DATA
        self.JOB_SEQUENCE = JOB_SEQUENCE
        self.BQ_CREATED_TIME = BQ_CREATED_TIME
        self.BQ_UPDATED_TIME = BQ_UPDATED_TIME
