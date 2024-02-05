class FuzzyComparisonResult:
    def __init__(
        self,
        UUID_Request: str = "",
        MISSION_NAME: str = "",
        JOB_ID: str = "",
        JOB_NAME: str = "",
        MATCH_TARGET:  str = "",
        COLUMN_DATA: str = "",
        SCORE: str = ""
    ):
        """
        初始化 FuzzyComparisonResult 實例並設定指定的參數。

        參數:
            UUID_Request (str): 任務的唯一識別碼。
            MISSION_NAME (str): 任務名稱。
            JOB_ID (str): 任務中工作的唯一識別碼。
            JOB_NAME (str): 工作名稱。
            MATCH_TARGET (str): 匹配目標。
            COLUMN_DATA (str): 欄位數據。
            SCORE (str): 匹配得分。
        """
        self.UUID_Request = UUID_Request
        self.MISSION_NAME = MISSION_NAME
        self.JOB_ID = JOB_ID
        self.JOB_NAME = JOB_NAME
        self.MATCH_TARGET = MATCH_TARGET
        self.COLUMN_DATA = COLUMN_DATA
        self.SCORE = SCORE
