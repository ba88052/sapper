from datetime import datetime


class RequestMessage:
    def __init__(
        self,
        ORDER_DATA: dict,
        MISSION_NAME: str,
        MISSION_ID: str,
        PREVIOUS_JOB_ID: str,
        JOB_ID: str,
        JOB_NAME: str,
        JOB_SEQUENCE: str,
        REPORT_PATH: str,
        SOURCE_TABLE_PATH: str,
        DESTINATION_TABLE_PATH: str,
        JOB_STATUS: str,
        USE_GENERAL_TMP_TABLE: str,
        BQ_CREATED_TIME: str,
        BQ_UPDATED_TIME: str,
    ):
        """
        初始化 RequestMessage 物件，設定各項任務相關參數。

        Args:
            ORDER_DATA (dict): 包含訂單詳細資訊的字典。
            MISSION_NAME (str, 可選): 表示任務名稱的字串。
            MISSION_ID (str, 可選): 代表任務唯一識別碼的字串。
            JOB_ID (str, 可選): 表示子任務唯一識別碼的字串。
            JOB_NAME (str, 可選): 代表子任務名稱的字串。
            JOB_SEQUENCE (str, 可選): 描述子任務在整體流程中的順序的字串。
            REPORT_PATH (str, 可選): 指向報告檔案位置的字串。
            SOURCE_TABLE_PATH (str, 可選): 指向源數據表位置的字串。
            DESTINATION_TABLE_PATH (str, 可選): 指向目標數據表位置的字串。
            JOB_STATUS (str, 可選): 描述當前任務狀態的字串。
            USE_GENERAL_TEMP_TABLE (str, 可選): 是否使用通用臨時表的字串。
            BQ_CREATED_TIME (datetime, 可選): 物件在 BigQuery 中的建立時間，預設為當前時間。
            BQ_UPDATED_TIME (datetime, 可選): 物件在 BigQuery 中的最後更新時間，預設為當前時間。
        """
        self.ORDER_DATA = ORDER_DATA
        self.MISSION_NAME = MISSION_NAME
        self.MISSION_ID = MISSION_ID
        self.PREVIOUS_JOB_ID = PREVIOUS_JOB_ID
        self.JOB_ID = JOB_ID
        self.JOB_NAME = JOB_NAME
        self.JOB_SEQUENCE = JOB_SEQUENCE
        self.REPORT_PATH = REPORT_PATH
        self.SOURCE_TABLE_PATH = SOURCE_TABLE_PATH
        self.DESTINATION_TABLE_PATH = DESTINATION_TABLE_PATH
        self.JOB_STATUS = JOB_STATUS
        self.USE_GENERAL_TMP_TABLE = USE_GENERAL_TMP_TABLE
        self.BQ_CREATED_TIME = BQ_CREATED_TIME
        self.BQ_UPDATED_TIME = BQ_UPDATED_TIME
