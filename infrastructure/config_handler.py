# config_handler.py
import json


def load_infra_config():
    """
    專門用來讀取infra config檔案
    """
    with open("./sapper_infra_config.json", "r") as file:
        return json.load(file)
    
INFRA_CONFIG = load_infra_config()

def load_monitoring_config():
    """
    專門用來讀取mission process config檔案
    """
    dataset_name = INFRA_CONFIG["bigquery"]["config"]["dataset_name"]
    monitoring_parameter_table_name = INFRA_CONFIG["bigquery"]["config"]["monitoring_parameter_table_name"]
    table_path = f"{dataset_name}.{monitoring_parameter_table_name}"
    config = INFRA_CONFIG(table_path).extract_last_config("PARAMETER")
    return config
    # with open("./monitoring_config.json", "r") as file:
    #     return json.load(file)
MONITORING_CONFIG = load_monitoring_config()
