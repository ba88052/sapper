class ApplicationInfraPort:
    def save_general_tmp_data(
        self, destination_table_path, general_tmp_data_entity, use_tmp_table
    ):
        """把實體化後的Entity資料，存入DB

        Args:
            destination_table_path(str): 要存進去的表格路徑
            general_tmp_data_entity (class): 要存進去的資料 entity
            use_tmp_table(str): 是否使用 tmp 表
        """
        pass

    def report_task_completed(self, report_return_path, report_message):
        """做完動作後，將完成task的訊息傳出

        Args:
            report_return_path (str): 回傳的管道
            report_message (str): 回報的message
        """
        pass
