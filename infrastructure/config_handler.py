# config_handler.py
import json


def load_infra_config():
    """
    專門用來讀取infra config檔案
    """
    with open("./sapper_infra_config.json", "r") as file:
        return json.load(file)


def load_monitoring_config():
    """
    專門用來讀取mission process config檔案
    """
    with open("./monitoring_config.json", "r") as file:
        return json.load(file)


INFRA_CONFIG = load_infra_config()
MONITORING_CONFIG = load_monitoring_config()
