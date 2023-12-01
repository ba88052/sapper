class ApplicationInfraPort:
    def save_destination_data_list(self, destination_table_path, destination_data_dict_list):
        """把實體化後的Entity資料，存入DB

        Args:
            raw_table_path(str): 要把raw_data存進去的表格路徑
            raw_data (class): 參照服務對應的raw_data_entity
        """
        pass

    def report_task_completed(self, report_return_path, report_message):
        """做完動作後，將完成task的訊息傳出

        Args:
            report_return_path (str): 回傳的管道
            report_message (str): 回報的message
        """
        pass
