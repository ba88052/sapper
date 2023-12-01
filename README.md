# DDD四層架構資料清洗程式 - raw_data_cleaner

raw_data_cleaner 是一個專門設計在 Google Cloud Platform（GCP）上運行的資料清理程式。它整合了 GCP 的Pub/Sub 和 Cloud Run，以實現數據的高效清理。
主要部署於 Cloud Run 並由 Pub/Sub 觸發

## 程式架構
該程式遵循 Domain-Driven Design (DDD) 的四層架構，包括以下層：

### Infrastructure
負責提供資料存取功能，例如與 Google Cloud 的 BigQuery 或其他存儲解決方案的連線。

### Domain
包含了業務邏輯以及應用程式的主要實體 (Entities)，例如各種cleaner的清理流程和控制邏輯。

### Application
負責調度 Domain 層和 Infrastructure 以處理特定的業務流程，並為 Interface 層提供所需的資料。

### Interfaces
提供與外部系統的交互功能，例如 RESTful API 或 Pub/Sub 消息處理。在此專案中，主要透過 Pub/Sub 觸發爬蟲運行。

## START
1. clone此專案到所需專案的workbench中：

\```bash
git clone <repository_url>
\```

2. 調整 `infra_config.json` 配置文件和 `deploy_to_cloudrun.sh` 中的專案名稱、BQ位置。

3. 部署至 Cloud Run：

\```bash
bash deploy_to_cloudrun.sh
\```

4. 在 GCP 建立對應的table，且需符合該資料清理對應之Entity文件

5. 設定訂閱項目皆為部屬之 cloud run，接著用pub/sub打入以下資料到cloud run中，以觸發爬蟲。
{
"job_name": "CLEAN_JOB_NAME",
 "parent_job_id": "ID"
}


## API 使用方式

此資料清洗程式提供了以下 API 端點，以允許外部系統，主要為pub/sub觸發爬蟲作業。

### 1. Automated Spider Updater (`/raw_data_cleaner`)
- **備註**
- **方法**: POST
- **描述**: 觸發自動資料清理。
- **請求參數**: JSON 物件，包含 `job_name` 字段和 `parent_job_id`字段。
- **回應**: 成功訊息及 204 狀態碼。
- **範例**:    
\```json
    {
      "job_name": "ssc_company_listing_info_spider",
      "parent_job_id": "5e858ef5-f5b2-47ec-b13b-2ce8f9cffff5"
    }
 \```



## 注意事項
- 由於此資料清洗程式完全在 GCP 上運行，因此不支援本地運行或測試。
- 請確保所有的 GCP 服務和資源都已正確配置，並修改 `infra_config.json`，和新增對應資料的清理方式於 raw_data_cleaner ，並包含對應的Entity。
- 若要新增清理程式，步驟可以如下：1. 增加entity. 2. 在BQ中建立表，並把表寫在infra_config裏面 3. 撰寫清理邏輯
