#!/bin/bash
#chmod +x deploy_to_cloudrun.sh

# 定義變數
REGION=asia-east1
GCP_PROJECT_ID=cdcda-lab-377808
REPO_NAME=sam-test
IMAGE_NAME=scout
CLOUD_RUN_SERVICE_NAMES=("scout") # 定義一個陣列
FULL_IMAGE_NAME=$REGION-docker.pkg.dev/$GCP_PROJECT_ID/$REPO_NAME/$IMAGE_NAME
SERVICE_ACCOUNT='sa-for-sam-liaw@cdcda-lab-377808.iam.gserviceaccount.com'

# Docker 認證
gcloud -q auth configure-docker $REGION-docker.pkg.dev

# 確認 Artifact Repository 是否已存在，否則建立
# if gcloud artifacts repositories list --project=$GCP_PROJECT_ID --location=$REGION | grep -q $REPO_NAME; then
#   echo "Artifact Repository $REPO_NAME already exists. Skipping creation."
# else
#   echo "Artifact Repository $REPO_NAME does not exist. Creating now..."
# gcloud artifacts repositories create $REPO_NAME \
# --repository-format=docker \
# --location=$REGION \
# --description="Docker repository for $REPO_NAME" \
# --project=$GCP_PROJECT_ID

# gcloud -q auth configure-docker $REGION-docker.pkg.dev
# fi

# 建立 Docker image
docker build -t $FULL_IMAGE_NAME .

# 將 Docker image 推送到儲存庫
docker push $FULL_IMAGE_NAME

for CLOUD_RUN_SERVICE_NAME in "${CLOUD_RUN_SERVICE_NAMES[@]}"; do
  # 檢查是否有設定服務帳戶，若無則使用預設服務帳戶
  # 參數設定包含 
  # 記憶體 (Memory): 使用 --memory 參數。
  # 要求逾時 (Timeout): 使用 --timeout 參數。
  # 每個執行個體的並行要求數量上限 (Concurrency): 使用 --concurrency 參數。
  # 執行個體數量上限 (Max Instances): 使用 --max-instances 參數。
  # 服務帳戶 (Service Account): 使用 --service-account 參數。
  if [ -z "$SERVICE_ACCOUNT" ]
  then
    gcloud run deploy $CLOUD_RUN_SERVICE_NAME \
      --image $FULL_IMAGE_NAME \
      --platform managed \
      --region $REGION \
      --memory 2Gi \
      --timeout 3600s \
      --concurrency 1 \
      --max-instances 10
  else
    gcloud run deploy $CLOUD_RUN_SERVICE_NAME \
      --image $FULL_IMAGE_NAME \
      --platform managed \
      --region $REGION \
      --service-account $SERVICE_ACCOUNT \
      --memory 2Gi \
      --timeout 3600s \
      --concurrency 1 \
      --max-instances 10
  fi
done

current_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "服務成功部署時間："$current_time