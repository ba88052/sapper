import json

from google.cloud import pubsub_v1
from google.auth import default


class PubSubClient:
    """
    讀取參數建立 PubSub Client
    """

    def __init__(self):
        # self.project = LIAISON_INFRA_CONFIG["pubsub"]["project_name"]
        _, project_id = default()
        self.project = project_id
        self.client = pubsub_v1.PublisherClient()
