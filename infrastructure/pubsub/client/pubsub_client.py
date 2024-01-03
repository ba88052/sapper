import json
from infrastructure.infra_config_handler import INFRA_CONFIG
from google.cloud import pubsub_v1


class PubSubClient:
    """
    讀取參數建立 PubSub Client
    """

    def __init__(self):
        self.project_id = INFRA_CONFIG["pubsub"]["project_name"]
        self.client = pubsub_v1.PublisherClient()
