from rapidfuzz import process, fuzz

from domain.domain_infra_port import DomainInfraPort
from domain.entity.general_tmp_data_entity import GeneralTmpData
from domain.entity.fuzzy_comparison_result_entity import FuzzyComparisonResult
from domain.service.job.job import Job

class FuzzyComparison(Job):
    def __init__(self, mission_id, mission_name, domain_infra_repository=DomainInfraPort()):
        """
        初始化 FuzzyComparison 類別。

        Args:
            mission_id (str): 任務 ID。
            mission_name (str): 任務名稱。
            domain_infra_repository (DomainInfraPort): 領域基礎設施存儲庫實例。
        """
        self.mission_id = mission_id
        self.mission_name = mission_name
        self.infra_repository = domain_infra_repository

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
        # === MODIFIED START: 2023-05-28 ===
        # 20240528 修改成直接從 compare_table_path 取得，前面不跑customize_select
        tmp_data = self.infra_repository.customize_select_from_source_table(
            source_table_path=source_table_path)
        print("tmp_data", tmp_data)
        # === MODIFIED END: 2023-05-28 ===
        
        # 確保 match_target 是一個列表
        match_target = order_data["match_target"]
        if not isinstance(match_target, list):
            match_target = [match_target]
        comparison_column = order_data["comparison_column"]
        fuzzy_comparison_result_dict_list = []
        closest_match_data_list = []

        # 精簡迴圈結構，減少重複計算
        # === MODIFIED START: 2023-05-28 ===
        for target in match_target:
            closest_matches_list = self.__find_closest_matches(match_target=target, data_dicts=tmp_data, comparison_column=comparison_column)
            for closest_matches in closest_matches_list:
                fuzzy_comparison_result_dict = {
                    "MATCH_TARGET": target,
                    "COLUMN_DATA": closest_matches[0],
                    "SCORE": closest_matches[1]
                }
                fuzzy_comparison_result_dict_list.append(fuzzy_comparison_result_dict)
            closest_match_data = next((item for item in tmp_data if item[comparison_column] == closest_matches_list[0][0]), None)
            closest_match_data["MATCH_TARGET"] = target
            closest_match_data_list.append(closest_match_data)
            closest_match_data_list = [dict(t) for t in {tuple(d.items()) for d in closest_match_data_list}]
        print("fuzzy_comparison_result_dict_list", fuzzy_comparison_result_dict_list)
        # === MODIFIED END: 2023-05-28 ===
        general_tmp_data_entity = GeneralTmpData(TMP_DATA=fuzzy_comparison_result_dict_list)

        
        print("closest_match_data_list", closest_match_data_list)
        closest_match_data_list = self.filter_today_results(closest_match_data_list = closest_match_data_list)

        print("closest_match_data_list_2", closest_match_data_list)
        return general_tmp_data_entity, closest_match_data_list

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
        column_data = [row[comparison_column] for row in data_dicts if comparison_column in row]
        closest_matches = self.__fuzzy_match(match_target, column_data, n=n)
        return closest_matches

    def __fuzzy_match(self, match_target, column_data, n):
        """
        使用 RapidFuzz 對一列數據進行模糊比對，並計算匹配分數。
        此方法使用了更快的模糊比對算法，並將結果排序返回。

        Args:
            match_target (str): 要進行比對的目標字符串。
            column_data (list of str): 要進行比對的數據列。
            n (int, optional): 要返回的最接近匹配項的數量。

        Returns:
            list of tuples: 包含最接近匹配項及其分數的列表。
        """
        results = process.extract(match_target, column_data, scorer=fuzz.QRatio, limit=n)
        sorted_matches = [(result[0], result[1]) for result in results]

        # 用 rapidfuzz 取代 difflib
        # match_scores = {item: difflib.SequenceMatcher(None, match_target, item).ratio() for item in column_data}
        # sorted_matches = sorted(match_scores.items(), key=lambda x: x[1], reverse=True)[:n]

        return sorted_matches
    
    # === MODIFIED START: 2023-08-15 ===
    def filter_today_results(self, closest_match_data_list):
        """
        根據今天的結果過濾 closest_match_data_list，只保留 MATCH_TARGET 和 COMPANY_NAME 都相同的項目，或 MATCH_TARGET 不同的項目。
        簡單來說，這是為了避免重複的結果，所以以客戶填寫的公司名稱（MATCH_TARGET）當作類似唯一ID
        如果比對的結果（在比對表是COLUMN_DATA，在記憶體中是COMPANY_NAME）一樣，且唯一ID不同，表示是重複的結果，所以拋棄。
        如果比對的結果一樣，但是MATCH_TARGET一樣，表示這是同一個ID，查詢FInancial跟Comany Info的結果，所以保留。
        之所以會這樣改，主要是卡在時程關係，更好的做法應該是有一張表在打出去API後，紀錄他打了什麼，之後每一次打之前都可以做比對。

        Returns:
            list: 經過過濾的新列表。
        """

        query = """
                SELECT
                    COLUMN_DATA,
                    MATCH_TARGET
                FROM (
                    SELECT
                        MATCH_TARGET,
                        COLUMN_DATA,
                        SCORE,
                        ROW_NUMBER() OVER (
                            PARTITION BY MATCH_TARGET
                            ORDER BY CAST(SCORE AS FLOAT64) DESC
                        ) as rn
                    FROM
                        `TRANS_EDEP_VIETDATA_DATASET.TMP_COMPANY_COMPARISON_RESULT`
                    WHERE
                        PARTITION_DATE BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 6 DAY) AND CURRENT_DATE()
                ) tmp
                WHERE rn = 1
        """
        
        # 執行查詢並獲取結果
        today_result = self.infra_repository.run_query(query)
        print("today_result", today_result)

        # 建立新的列表，只保留符合條件的項目
        new_closest_match_data_list = []
        
        for item in closest_match_data_list:
            match_company_name = item["COMPANY_NAME"]
            match_target = item["MATCH_TARGET"]
            print(match_company_name, match_target)
            
            # 檢查這包中的 company_name 中是否有對應的 COLUMN_DATA 
            matching_items = [
                today_item for today_item in today_result
                if today_item["COLUMN_DATA"] == match_company_name
            ]
            
            print(matching_items)
            if matching_items:
                # 如果 COLUMN_DATA 找到匹配，再檢查 MATCH_TARGET，如果一樣則保留
                if any(today_item["MATCH_TARGET"] == match_target for today_item in matching_items):
                    new_closest_match_data_list.append(item)
            else:
                # 如果 COLUMN_DATA 不存在匹配項目，保留該company_name
                new_closest_match_data_list.append(item)

        return new_closest_match_data_list
    # === MODIFIED END: 2023-08-15 ===