from application.application_infra_port import ApplicationInfraPort
from infrastructure.bigquery.repository.destination_table_repository import (
    DestinationTableRepository,
)
from infrastructure.pubsub.repository.report_task_completed_repository import (
    ReportTaskCompletedRepository,
)


class ApplicationRespositoryAdapter(ApplicationInfraPort):
    def __init__(self):
        pass

    def report_task_completed(self, report_return_path, report_message):
        """做完動作後，將完成task的訊息傳出

        Args:
            report_return_path (str): 回傳的管道
            report_message (str): 回報的message
        """
        return ReportTaskCompletedRepository().publish_message(
            report_return_path=report_return_path, message=report_message
        )

    def save_general_tmp_data(
        self, destination_table_path, general_tmp_data_entity, use_tmp_table
    ):
        """把實體化後的Entity資料，存入DB

        Args:
            raw_table_path(str): 要把raw_data存進去的表格路徑
            raw_data (class): 參照服務對應的raw_data_entity
        """
        DestinationTableRepository(destination_table_path=destination_table_path).save(
            general_tmp_data_entity=general_tmp_data_entity, use_tmp_table=use_tmp_table
        )
