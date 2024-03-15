import difflib
import json

from domain.domain_infra_port import DomainInfraPort
from domain.entity.general_tmp_data_entity import GeneralTmpData
from domain.entity.fuzzy_comparison_result_entity import FuzzyComparisonResult
from domain.service.job.job import Job


class FuzzyComparison(Job):
    def __init__(self, mission_id, mission_name, domain_infra_respository=DomainInfraPort()):
        """
        初始化 FuzzyComparison 類別。

        Args:
            mission_id (str): 任務 ID。
            mission_name (str): 任務名稱。
            domain_infra_respository (DomainInfraPort): 領域基礎設施存儲庫實例。
        """
        self.mission_id = mission_id
        self.mission_name = mission_name
        self.infra_respository = domain_infra_respository

    def execute(self, order_data, source_table_path, previous_job_id):
        """
        執行模糊比對任務。

        Args:
            order_data (dict): 包含比對目標和比對列名的訂單數據。
            source_table_path (str): 來源表格的路徑。
            previous_job_id (str): 前一任務的 ID。

        Returns:
            GeneralTmpData: 包含最接近匹配項的臨時數據實體。
        """
        tmp_table_data_list = self.infra_respository.get_general_tmp_table_data(
            source_table_path=source_table_path, previous_job_id=previous_job_id
        )
        match_target = order_data["match_target"]
        comparison_column = order_data["comparison_column"]
        fuzzy_comparison_result_dict_list = []

        for tmp_table_data in tmp_table_data_list:
            tmp_data_list = tmp_table_data["TMP_DATA"]
            tmp_data_list_converted = json.loads(tmp_data_list)
            tmp_data = tmp_data_list_converted
            closest_matches_list = self.__find_closest_matches(match_target=match_target, data_dicts=tmp_data, comparison_column=comparison_column)
            for closest_matches in closest_matches_list:
                fuzzy_comparison_result_dict = {
                    "UUID_Request":tmp_table_data["UUID_Request"],
                    "MISSION_NAME":tmp_table_data["MISSION_NAME"],
                    "JOB_ID":tmp_table_data["JOB_ID"],
                    "JOB_NAME":tmp_table_data["JOB_NAME"],
                    "MATCH_TARGET":match_target,
                    "COLUMN_DATA":closest_matches[0],
                    "SCORE":closest_matches[1]
                }
                fuzzy_comparison_result_dict_list.append(fuzzy_comparison_result_dict)
            print (fuzzy_comparison_result_dict_list)
        general_tmp_data_entity = GeneralTmpData(TMP_DATA=fuzzy_comparison_result_dict_list)
        return general_tmp_data_entity

    def __find_closest_matches(self, match_target, data_dicts, comparison_column, n=100):
        """
        在字典列表中的指定列找到與比較目標字符串最接近的幾個字符串。

        Args:
            match_target (str): 要進行比對的目標字符串。
            data_dicts (list of dict): 包含比對數據的字典列表。
            comparison_column (str): 要進行比對的列名。
            n (int, optional): 要返回的最接近匹配項的數量。預設為 100。

        Returns:
            list of tuples: 包含最接近匹配項及其分數的列表。
        """
        # print("data_dicts:", data_dicts)
        column_data = [row[comparison_column] for row in data_dicts if comparison_column in row]
        closest_matches = self.__fuzzy_match(match_target, column_data, n=n)
        return closest_matches

    def __fuzzy_match(self, match_target, column_data, n):
        """
        使用 difflib 對一列數據進行模糊比對，並計算匹配分數。

        Args:
            match_target (str): 要進行比對的目標字符串。
            column_data (list of str): 要進行比對的數據列。
            n (int, optional): 要返回的最接近匹配項的數量。

        Returns:
            list of tuples: 包含最接近匹配項及其分數的列表。
        """
        match_scores = {item: difflib.SequenceMatcher(None, match_target, item).ratio() for item in column_data}
        sorted_matches = sorted(match_scores.items(), key=lambda x: x[1], reverse=True)[:n]
        return sorted_matches
