# import json

# from infrastructure.bigquery.client.bq_client import BqClient
# from infrastructure.infra_config_handler import CONFIG


# class ApiLogRepository(BqClient):
#     """
#     負責涉及 api_log 表格的操作
#     """

#     def __init__(self):
#         super().__init__()
#         self.dataset = CONFIG["bigquery"]["dataset_name"]
#         self.table = CONFIG["bigquery"]["log"]["api_log_table_name"]
#         self.bigquery_table_id = f"{self.project}.{self.dataset}.{self.table}"

#     def save(self, api_log):
#         """
#         api_log 存到bq

#         Args:
#             api_log (api_log實體)
#         """
#         api_log_dict = self.__convert_api_log_entity_to_bq_format(api_log)
        
#         print(api_log_dict)

#         insertion_errors = self.client.insert_rows_json(
#             self.bigquery_table_id, [api_log_dict]
#         )
#         if insertion_errors:
#             print(
#                 f"Errors occurred while storing api_log to BigQuery: {insertion_errors}"
#             )
#         else:
#             print(
#                 "api_log stored successfully to BigQuery.")

#     def __convert_api_log_entity_to_bq_format(self, api_log):
#         """
#         把entity轉換成可以存入BQ的格式

#         Args:
#             api_log (api_log實體)

#         Returns:
#             dict: 可存入BQ的格式
#         """
#         # # 將 datetime 對象轉換為 RFC 3339 格式的字符串
#         start_time = api_log.Start_Time.strftime(
#             "%Y-%m-%dT%H:%M:%S.%fZ"
#         )
#         end_time = api_log.End_Time.strftime(
#             "%Y-%m-%dT%H:%M:%S.%fZ"
#         )
#         # 創建一個字典，並確保每個值都符合格式
#         bq_dict = {
#             "UUID_Request": str(api_log.UUID_Request),
#             "API_Type": str(api_log.API_Type),
#             "API_Name": str(api_log.API_Name),
#             "Start_Time": start_time,
#             "End_Time": end_time,
#             "Status_Code": str(api_log.Status_Code),
#             "Status_Detail": str(api_log.Status_Detail),
#             "Retry": int(api_log.Retry),
#         }
#         return bq_dict
