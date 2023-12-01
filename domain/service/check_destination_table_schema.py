from domain.domain_infra_port import DomainInfraPort

class CheckDestinationTableSchema():
    def __init__(self, domain_infra_respository = DomainInfraPort()):
        self.domain_infra_respository = domain_infra_respository


    def fill_missing_fields(table_id, json_data):
        client = bigquery.Client()

        # 獲取 BigQuery 表的 schema
        table = client.get_table(table_id)
        schema_field_names = {field.name for field in table.schema}

        # 比對 JSON 資料與 schema，填充缺失的欄位
        filled_data = []
        for record in json_data:
            filled_record = {field: record.get(field, "") for field in schema_field_names}
            filled_data.append(filled_record)

        return filled_data

    # 使用範例
    table_id = "your-project.your_dataset.your_table"
    json_data = [
        {"column1": "value1", "column2": "value2"},
        # ... 其他記錄
    ]

    filled_data = fill_missing_fields(table_id, json_data)
    print(filled_data)