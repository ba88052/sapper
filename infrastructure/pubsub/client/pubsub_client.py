import json

from google.cloud import pubsub_v1

from infrastructure.config_handler import INFRA_CONFIG


class PubSubClient:
    """
    讀取參數建立 PubSub Client
    """

    def __init__(self):
        self.project_id = INFRA_CONFIG["pubsub"]["project_name"]
        self.client = pubsub_v1.PublisherClient()
