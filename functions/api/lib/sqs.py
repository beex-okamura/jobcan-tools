import json

import boto3  # type: ignore

from lib.environment import get_environment

env = get_environment()


class SQSClient:
    def __init__(self):
        self.client = boto3.client("sqs", region_name="ap-northeast-1", endpoint_url=env.endpoint_url)

    def send_punch_clock_message(self, user_id: str):
        self._send_message(env.punch_work_queue_url, json.dumps({"user_id": user_id}))

    def _send_message(self, queue_url, message):
        self.client.send_message(QueueUrl=queue_url, MessageBody=message)
