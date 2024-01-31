import difflib
import json

from domain.domain_infra_port import DomainInfraPort
from domain.entity.general_tmp_data_entity import GeneralTmpData
from domain.service.job.job import Job

class FuzzyComparison(Job):
    def __init__(
        self, mission_id, mission_name, domain_infra_respository=DomainInfraPort()
    ):
        self.mission_id = mission_id
        self.mission_name = mission_name
        self.infra_respository = domain_infra_respository

    def execute(self, order_data, source_table_path, previous_job_id):
        tmp_table_data_list = self.infra_respository.get_general_tmp_table_data(
            source_table_path=source_table_path, previous_job_id=previous_job_id
        )
        closest_matches_list = []
        # 要比對的資料
        match_target = order_data["match_target"]
        comparison_column = order_data["comparison_column"]

        for tmp_table_data in tmp_table_data_list:
            print("tmp_table_data", tmp_table_data)
            tmp_data_list = tmp_table_data["TMP_DATA"]
            tmp_data_list_converted = json.loads(tmp_data_list)
            tmp_data = tmp_data_list_converted[0]
            print("tmp_data", tmp_data)
            closest_matches = self.__find_closest_matches(match_target=match_target, data_dicts=tmp_data, comparison_column=comparison_column)
            closest_matches_list.append(closest_matches)
        general_tmp_data_entity = GeneralTmpData(TMP_DATA=closest_matches_list)
        return general_tmp_data_entity

    def __find_closest_matches(self, match_target, data_dicts, comparison_column, n=3):
        """
        在字典列表中的指定列找到與輸入字符串最接近的幾個字符串。
        """
        # 提取指定列的数据
        column_data = [row[comparison_column] for row in data_dicts if comparison_column in row]

        closest_matches = self.__fuzzy_match(match_target, column_data, n=n)
        return closest_matches

    def __fuzzy_match(self, match_target, column_data, n=3):
        """
        使用 difflib 對一列數據進行比對，並計算匹配分數。
        """
        # 计算每个字符串与输入字符串的匹配分数
        match_scores = {item: difflib.SequenceMatcher(None, match_target, item).ratio() for item in column_data}

        # 根据匹配分数排序并获取最高的n个匹配项
        sorted_matches = sorted(match_scores.items(), key=lambda x: x[1], reverse=True)[:n]

        return sorted_matches