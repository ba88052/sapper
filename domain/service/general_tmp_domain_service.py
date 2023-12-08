from datetime import datetime

from domain.entity.general_tmp_data_entity import GeneralTmpData


class GeneralTmpDataDomainService:
    def get_gemeral_tmp_data(
        self,
        UUID_Request: dict = {},
        MISSION_NAME: str = "",
        TASK_ID: str = "",
        TASK_NAME: str = "",
        TASK_SEQUENCE: str = "",
        TMP_DATA: list = [],
        BQ_CREATED_TIME: str = "",
        BQ_UPDATED_TIME: str = "",
    ):
        """
        輸入參數，回傳 RequestMessage 的entity

        Args:
            ORDER_DATA (dict): 包含訂單詳細資訊的字典。
            MISSION_NAME (str, 可選): 表示任務名稱的字串。
            MISSION_ID (str, 可選): 代表任務唯一識別碼的字串。
            TASK_ID (str, 可選): 表示子任務唯一識別碼的字串。
            TASK_NAME (str, 可選): 代表子任務名稱的字串。
            TASK_SEQUENCE (str, 可選): 描述子任務在整體流程中的順序的字串。

            USE_GENERAL_TEMP_TABLE (str, 可選): 是否使用通用臨時表的字串。
            BQ_CREATED_TIME (datetime, 可選): 物件在 BigQuery 中的建立時間，預設為當前時間。
            BQ_UPDATED_TIME (datetime, 可選): 物件在 BigQuery 中的最後更新時間，預設為當前時間。

        Returns:
            request_message實體
        """
        return GeneralTmpData(
            UUID_Request=UUID_Request,
            MISSION_NAME=MISSION_NAME,
            TASK_ID=TASK_ID,
            TASK_NAME=TASK_NAME,
            TASK_SEQUENCE=TASK_SEQUENCE,
            TMP_DATA=TMP_DATA,
            BQ_CREATED_TIME=BQ_CREATED_TIME,
            BQ_UPDATED_TIME=BQ_UPDATED_TIME,
        )
