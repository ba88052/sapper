# config_handler.py
import json


def load_config():
    """
    專門用來讀取檔案，其他需要config的程式，只需import此程式
    """
    with open("./config.json", "r") as file:
        return json.load(file)


CONFIG = load_config()
