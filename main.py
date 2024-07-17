import os

from flask import Flask, g, request

from infrastructure.application_infra_adapter import ApplicationRepositoryAdapter
from infrastructure.domain_infra_adapter import DomainRepositoryAdapter
from interfaces import api_routes

# from infrastructure.database.domain_database_repository_adapter import DomainRespositoryAdapter

app = Flask(__name__)
app.register_blueprint(api_routes.routes)


@app.before_request
def setup_global_objects():
    g.APPLICATION_INFRA_ADAPTOR = ApplicationRepositoryAdapter()
    g.DOMAIN_INFRA_ADAPTER = DomainRepositoryAdapter()


# g.CLEANE_DATA_ADAPTOR = DomainRespositoryAdapter()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# from flask import Flask, request, jsonify
# import os
# import time
# import pandas as pd
# from google.cloud import bigquery
# from google.cloud.exceptions import GoogleCloudError
# import gzip

# app = Flask(__name__)

# @app.route("/sapper/execute_table_transform_job", methods=["POST"])
# def process_data():
#     try: 
#         print("Start")
#         client = bigquery.Client()

#          # 1. 从Excel读取数据并插入到BigQuery表中
#         # df = pd.read_excel("./company_name_tax_code_vietdata.xlsx")
#         # df.columns = ["TAX_CODE", "COMPANY_NAME"]
#         # table_id = 'EDEP_DATA_TRANSFORMER_DATASET.COMPANY_TAX_MAPPING'
#         # records = df.to_dict('records')
#         # errors = client.insert_rows_json(table_id, records)
#         # if errors:
#         #     return jsonify({"error": errors}), 500
#         # 2. 执行一系列的SQL插入操作（示例）
#         # 注意：以下代码仅为示例，实际使用时需要根据你的需求调整SQL语句和执行方式
#         sql_statements = [
#             # 这里添加你的SQL插入语句
# """
# INSERT INTO `EDEP_DATA_TRANSFORMER_DATASET.MONITORING_PARAMETER` (PARAMETER_ID, PARAMETER, BQ_CREATED_TIME, BQ_UPDATED_TIME)
# VALUES
# (
#     '1',
#     '''
# {
#     "flow_mapping":{
#         "scout" : "E01",
#         "sapper": "E02",
#         "liaison": "E03"
#         },
#     "task_mapping":{
#         "scout":{            
#             "select_job":"01",
#             "run_job":"02",
#             "add_shared_data":"03",
#             "save_data":"04",
#             "report_job":"05",
#             "notice_job_success":"11"
#             },
#         "sapper":{
#             "select_job":"01",
#             "run_job":"02",
#             "add_shared_data":"03",
#             "save_data":"04",
#             "report_job":"05",
#             "notice_job_success":"11"
#             },
#         "liaison":{
#             "get_mission_process_config_data":"01",
#             "save_previous_job_status_log":"02",
#             "generator_next_job_command":"03",
#             "save_next_job_status_log":"04",
#             "send_next_job_command":"05",
#             "report_mission_status":"06",
#             "notice_job_success":"11"
#             }
#         },
#     "severity_mapping":{
#         "INFO":"00",
#         "NOTICE":"01",
#         "DEBUG":"44",
#         "ERROR":"99"
#         }
# }
    
#     ''',
#     '2024-04-09T10:26:21.614867',
#     '2024-04-09T10:26:21.614867'
# );
# """
# """
#  DELETE FROM `EDEP_DATA_TRANSFORMER_DATASET.COMPANY_TAX_MAPPING` WHERE TRUE
# """]
#         for sql in sql_statements:
#             try:
#                 query_job = client.query(sql)  # 执行SQL
#                 print(query_job.result())  # 等待结果
#             except:
#                 continue
#         print('SQL complete.')
#         batch_size = 5000
#         csv_file = 'output.csv.gz'

#         with gzip.open(csv_file, 'rt', encoding='utf-8') as f:
#             df_iter = pd.read_csv(f, chunksize=batch_size)

#             for df in df_iter:
#                 # 將 DataFrame 轉換為 JSON 格式，以便插入 BigQuery
#                 df.columns = ["TAX_CODE", "COMPANY_NAME"]
#                 records = df.to_dict(orient='records')

#                 # 建立插入作業
#                 errors = client.insert_rows_json(f'EDEP_DATA_TRANSFORMER_DATASET.COMPANY_TAX_MAPPING', records)
#                 time.sleep(1)

#                 if errors:
#                     print(f'Encountered errors while inserting rows: {errors}')
#                 else:
#                     print(f'Successfully inserted {len(records)} rows.')

#         print('Data insertion complete.')
#         return jsonify({"message": "Data processing completed successfully"}), 200
#     except exceptions as e:
#         print({"error": str(e)})
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     # start()
#     app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
