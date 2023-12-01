import json

from infrastructure.pubsub.client.pubsub_client import PubSubClient

class ReportTaskCompletedRepository(PubSubClient):
    def publish_message(self, report_return_path, message, attributes={}):
        """
        負責把訊息打到 report_return_path 

        Returns:
            str: 傳出去後pub/sub回傳的訊息
        """
        message = json.dumps(message, default=str)
        data = message.encode("utf-8")
        topic_path = self.client.topic_path(self.project_id, report_return_path)
        print(data)
        future = self.client.publish(topic_path, data, **attributes)
        return future.result()
