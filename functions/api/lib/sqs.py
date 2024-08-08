import boto3  # type: ignore

from lib.environment import get_environment
from schemas.scraping_payload import ScrapingPayload


env = get_environment()


class SQSClient:
    def __init__(self):
        self.client = boto3.client("sqs", region_name="ap-northeast-1", endpoint_url=env.endpoint_url)

    def send_punch_clock_message(self, payload: ScrapingPayload):
        self._send_message(env.punch_work_queue_url, payload.model_dump_json())

    def _send_message(self, queue_url, message):
        self.client.send_message(QueueUrl=queue_url, MessageBody=message)
