from datetime import datetime

class RequestMessage:
    def __init__(
        self,
        ORDER_DATA: dict,
        MISSION_NAME: str,
        MISSION_ID: str,
        PREVIOUS_TASK_ID :str,
        TASK_ID: str,
        TASK_NAME: str,
        TASK_SEQUENCE: str,
        REPORT_PATH: str,
        SOURCE_TABLE_PATH: str,
        DESTINATION_TABLE_PATH: str,
        TASK_STATUS: str,
        USE_GENERAL_TEMP_TABLE: str,
        BQ_CREATED_TIME: str,
        BQ_UPDATED_TIME: str
    ):
        """
        初始化 RequestMessage 物件，設定各項任務相關參數。

        Args:
            ORDER_DATA (dict): 包含訂單詳細資訊的字典。
            MISSION_NAME (str, 可選): 表示任務名稱的字串。
            MISSION_ID (str, 可選): 代表任務唯一識別碼的字串。
            TASK_ID (str, 可選): 表示子任務唯一識別碼的字串。
            TASK_NAME (str, 可選): 代表子任務名稱的字串。
            TASK_SEQUENCE (str, 可選): 描述子任務在整體流程中的順序的字串。
            REPORT_PATH (str, 可選): 指向報告檔案位置的字串。
            SOURCE_TABLE_PATH (str, 可選): 指向源數據表位置的字串。
            DESTINATION_TABLE_PATH (str, 可選): 指向目標數據表位置的字串。
            TASK_STATUS (str, 可選): 描述當前任務狀態的字串。
            USE_GENERAL_TEMP_TABLE (str, 可選): 是否使用通用臨時表的字串。
            BQ_CREATED_TIME (datetime, 可選): 物件在 BigQuery 中的建立時間，預設為當前時間。
            BQ_UPDATED_TIME (datetime, 可選): 物件在 BigQuery 中的最後更新時間，預設為當前時間。
        """
        self.ORDER_DATA = ORDER_DATA
        self.MISSION_NAME = MISSION_NAME
        self.MISSION_ID = MISSION_ID
        self.PREVIOUS_TASK_ID = PREVIOUS_TASK_ID
        self.TASK_ID = TASK_ID
        self.TASK_NAME = TASK_NAME
        self.TASK_SEQUENCE = TASK_SEQUENCE
        self.REPORT_PATH = REPORT_PATH
        self.SOURCE_TABLE_PATH = SOURCE_TABLE_PATH
        self.DESTINATION_TABLE_PATH = DESTINATION_TABLE_PATH
        self.TASK_STATUS = TASK_STATUS
        self.USE_GENERAL_TEMP_TABLE = USE_GENERAL_TEMP_TABLE
        self.BQ_CREATED_TIME = BQ_CREATED_TIME 
        self.BQ_UPDATED_TIME = BQ_UPDATED_TIME 
