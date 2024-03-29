from datetime import datetime

# 優化建議：考慮將臨時數據存儲至 Google Cloud Storage (GCS)，或修改架構以一次只處理一筆數據。

class GeneralTmpData:
    def __init__(
        self,
        UUID_Request: str = "",
        MISSION_NAME: str = "",
        JOB_ID: str = "",
        JOB_NAME: str = "",
        TMP_DATA: list = [],
        JOB_SEQUENCE: str = "",
    ):
        """
        初始化 GeneralTmpData 實例並設定指定的參數。

        參數:
            UUID_Request (str): 任務的唯一識別碼。
            MISSION_NAME (str): 任務名稱。
            JOB_ID (str): 任務中工作的唯一識別碼。
            JOB_NAME (str): 工作名稱。
            TMP_DATA (list): 用於臨時存儲與工作相關的數據的列表。
            JOB_SEQUENCE (str): 工作在任務中的順序或排序。
        """
        self.UUID_Request = UUID_Request
        self.MISSION_NAME = MISSION_NAME
        self.JOB_ID = JOB_ID
        self.JOB_NAME = JOB_NAME
        self.TMP_DATA = TMP_DATA
        self.JOB_SEQUENCE = JOB_SEQUENCE
