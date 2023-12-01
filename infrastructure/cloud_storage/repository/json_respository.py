from infrastructure.cloud_storage.client.gcs_client import GcsClient
import json

class JsonRepository(GcsClient):
    def __init__(self):
        super().__init__()

    def upload_text(self, raw_table, raw_table_bucket_name, raw_table_blob_name):
        """
        將資料上傳到 GCS，資料可以是字典或文本字符串

        Args:
            data (dict or str): 要上傳的資料，可以是字典或字符串格式
            destination_blob_name (str): blob 名稱
        """
        
        data = raw_table.RawData
        self.bucket = self.client.get_bucket(raw_table_bucket_name)
        blob = self.bucket.blob(raw_table_blob_name)

        # 如果 data 是字典，則將其轉換為 JSON 字符串
        if isinstance(data, dict):
            data_string = json.dumps(data, ensure_ascii=False, indent=4)
        elif isinstance(data, str):
            data_string = data
        else:
            raise TypeError("data 必須是 dict 或 str 類型")

        blob.upload_from_string(data_string, content_type="text/plain")
        print(f"資料已上傳到 {raw_table_blob_name}。")

    def download_json(self, blob_name):
        """
        从 GCS bucket 下載 JSON 

        Args:
            blob_name (str): blob 名稱

        Returns:
            dict: dict
        """
        blob = self.bucket.blob(blob_name)
        json_string = blob.download_as_text()
        json_data = json.loads(json_string)
        return json_data
