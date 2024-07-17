import json

from google.cloud import storage
from google.auth import default


class GcsClient:
    """
    讀取參數建立 GCS Client
    """

    def __init__(self):
        _, project_id = default()
        self.project = project_id
        # self.project = LIAISON_INFRA_CONFIG["gcs"]["project_name"]
        self.client = storage.Client()
        # self.bucket = self.client.get_bucket(CONFIG["gcs"]["bucket_name"])
