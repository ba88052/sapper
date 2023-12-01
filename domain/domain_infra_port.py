class DomainInfraPort:
    def save_api_log_entity_list(self, api_log_entity_list):
        """把實體化後的Entity資料，存入DB

        Args:
            api_log_entity_list (list): 參照api_log_entity
        """
        pass

    def get_config(self):
        """
        讀取參數檔
        """
        raise NotImplementedError
    
    def run_query(self):
        """
        跑 query
        """
        pass

    def get_table_schema(self, table_path):
        """
        獲得指定Table的Schema

        Args:
            table_path (str): Table的路徑
        """
        pass
        
