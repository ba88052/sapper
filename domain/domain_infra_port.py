class DomainInfraPort:
    def get_infra_config(self):
        """
        讀取參數檔
        """
        raise NotImplementedError

    def get_monitoring_config(self):
        """
        讀取 monitoring 參數檔
        """
        return NotImplementedError

    def customize_select_from_source_table(self, source_table_path, conditions=None):
        """
        客製化查詢source_table

        Args:
            source_table_path (_type_): _description_
            conditions (_type_): _description_
        """
        pass

    def get_general_tmp_table_data(self, source_table_path, previous_job_id):
        """
        獲取tmp table 的 data

        Args:
            source_table_path (_type_): _description_
        """
        pass

    def save_flow_log(self, flow_log_entity):
        """
        存 flow_log ，還需要發送 logging 到對應服務中做紀錄
        """
        pass
    
    def run_query(self, query):
        pass