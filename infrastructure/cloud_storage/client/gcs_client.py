import json

from google.cloud import storage

from infrastructure.config_handler import INFRA_CONFIG


class GcsClient:
    """
    讀取參數建立 GCS Client
    """

    def __init__(self):
        self.project = CONFIG["gcs"]["project_name"]
        self.client = storage.Client(self.project)
        # self.bucket = self.client.get_bucket(CONFIG["gcs"]["bucket_name"])
