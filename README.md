# Sapper 微服務

## 優化方向
1. infra 層拆成存 entity 存 json的，統一接口，然後讓adapter去做邏輯與傳參數和資料，
2. 文件要寫如何新增新功能，如何改動邏輯。

## 服務概述

Sapper 微服務專門用於資料的清理與整理，實現從一個數據表到另一個數據表的數據轉換。此服務利用 Google Cloud Platform 的功能，特別是 BigQuery 和 Pub/Sub，以實現高效的數據處理。

## 系統架構

Sapper 微服務採用 DDD 四層架構：

1. **應用層（Application）**：處理接收到的任務訊息並控制數據處理流程。
2. **領域層（Domain）**：包含數據轉換的業務邏輯和數據模型。
3. **基礎設施層（Infrastructure）**：提供與 GCP 服務的整合，如數據庫和消息隊列。
4. **接口層（Interfaces）**：處理來自外部的請求並定義 API 端點。

## 主要entity

## 安裝指南
### START
1. clone此專案到所需專案的workbench中：

    ```bash
    git clone <repository_url>
    ```

2. 調整 `infra_config.json` 配置文件和 `deploy_to_cloudrun.sh` 中的專案名稱、BQ位置。

3. 部署至 Cloud Run：

    ```bash
    bash deploy_to_cloudrun.sh
    ```

4. 在 GCP 建立對應的table，且需符合該資料清理對應之Entity文件。

5. 設定訂閱項目皆為部屬之 cloud run，接著用pub/sub打入資料到cloud run中，以觸發程式。


## API 使用說明

Sapper 微服務提供以下 API 接口：
- `POST /sapper/execute_table_transform_job`: 接收來自 Pub/Sub 的訊息，執行資料轉換任務。

測試用訊息：
做客製化select
{
  "order_data": {
    "select_conditions": ["TASK_ID = '{previous_task_id}'"]
  },
  "mission_name": "seon_test",
  "mission_id": "mission_test_1206",
  "task_name": "customize_select",
  "task_id": "cus_select_test",
  "previous_task_id": "755ab57c-b55f-45cf-8a32-073001e0c463",
  "task_sequence": 2,
  "task_report_path": "repot_liaison",
  "source_table_path": "SAM_LAB.MISSION_NAME_RAW_TABLE_test_1129",
  "destination_table_path": "SAM_LAB.SAPPER_GENERAL_TMP_TABLE_test_1206",
  "task_status": "start",
  "use_general_tmp_table": true
}

做json攤平
{
  "order_data": {
    "columns": "RAW_DATA"
  },
  "mission_name": "seon_test",
  "mission_id": "mission_test_1206",
  "task_name": "flatten_json",
  "task_id": "flat_json_test",
  "previous_task_id":"cus_select_test",
  "task_sequence": 3,
  "report_path": "repot_liaison",
  "source_table_path": "SAM_LAB.SAPPER_GENERAL_TMP_TABLE_test_1206",
  "destination_table_path" : "SAM_LAB.SEON_TEST_1208",
  "task_status": "start",
 "use_general_tmp_table": false
}

## 注意事項
- 確保所有必要的 GCP 服務已被正確配置。
- 在生產環境中部署前進行充分測試。

## 版本歷史
- v1.0.0：初始版本。