from domain.service.task.task import Task
from domain.domain_infra_port import DomainInfraPort
from domain.service.general_tmp_domain_service import GeneralTmpDataDomainService
import json


class FlattenJson(Task):
    def __init__(self, mission_id, mission_name, domain_infra_respository=DomainInfraPort()):
        self.mission_id = mission_id
        self.mission_name = mission_name
        self.infra_respository = domain_infra_respository

    def execute(self, order_data, source_table_path, previous_task_id):
        """
        將巢狀Json轉換為扁平字典。
        """
        flatten_json_data_list = []
        tmp_table_data_list = self.infra_respository.get_general_tmp_table_data(source_table_path = source_table_path, 
                                                                           previous_task_id = previous_task_id)
        for tmp_table_data in tmp_table_data_list:
            tmp_data_list = tmp_table_data["TMP_DATA"]
            tmp_data_list = json.loads(tmp_data_list)
            print("tmp_data_list", tmp_data_list)
            for tmp_data in tmp_data_list:
                print("tmp_data", tmp_data)
                flatten_json_data = self.__flatten(data = tmp_data[order_data["columns"]])
                flatten_json_data = self.__convert_all_to_str(flatten_json_data)
                flatten_json_data_list.append(flatten_json_data)

        general_tmp_data_entity = GeneralTmpDataDomainService().get_gemeral_tmp_data(
            TMP_DATA = flatten_json_data_list
            )
        return general_tmp_data_entity
    
    def __flatten(self, data, parent_key='', sep='_'):
        """
        將巢狀字典轉換為扁平字典。
        這個函數會遞迴地遍歷巢狀字典，並生成一個新的字典，其中所有的Key都是通過連接父鍵和子鍵而得到的。

        args:
            data (dict): 要扁平化的嵌套字典。
            parent_key (str, 可選): 當前的父鍵。預設是空字符串。
            sep (str, 可選): 用於連接父鍵和子鍵的分隔符。預設是下劃線 ('_')。

        return:
            dict: 扁平化後的字典，其中每個key都是通過連接父鍵和子鍵而得到的，並且所有的值都不是字典。
        """
        items = {}  # 初始化空字典，用於存儲扁平化後的結果。
        for k, v in data.items():  # 遍歷輸入字典中的所有項。
            new_key = f"{parent_key}{sep}{k}" if parent_key else k  # 構造新的鍵，將父鍵和當前的鍵連接起來。
            if isinstance(v, dict):  # 檢查當前的值是否是字典。
                items.update(self.__flatten(v, new_key, sep=sep))  # 如果是，則遞迴調用 flatten 函數來繼續扁平化。
            else:
                items[new_key] = v  # 如果不是，則直接將新的鍵和值添加到結果字典中。
        return items  # 返回填充了扁平化結果的字典。

    def __convert_all_to_str(self, data): 
        """
        將資料使用以下程式碼，把欄位都轉成str

        Args:
            data (dict): dict

        Returns:
            data (dict): dict 轉換成裡面都 str
        """
        if isinstance(data, dict):
            return {k: self.__convert_all_to_str(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.__convert_all_to_str(v) for v in data]
        else:
            return str(data)
