import boto3
import json
import urllib.parse as url_parse

from . import AbstractQueue, QueueMessage

class Sqs(AbstractQueue):
    def __init__(self, uri, host_url, subdomain, endpoint_url=None, client_kwargs={}):
        parts = url_parse.urlparse(uri)
        self.scheme = parts.scheme
        aws_access_key_id = parts.username
        aws_secret_access_key = parts.password
        host = parts.hostname
        path = parts.path
        self.set_host_url(host_url) \
            .set_subdomain(subdomain)

        host_parts = host.split('.', 2)
        self.region = host_parts[1]
        self.sqs_client = boto3.client(
            'sqs',
            region_name=self.region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=endpoint_url,
            **client_kwargs,
        )

        path_parts = path.split('/')
        # Removing empty string from list
        path_parts = list(filter(None, path_parts))
        self.account_id = path_parts[0]
        self.queue_prefix = path_parts[1]

    def get_queue_url(self):
        return (
            self.scheme + '://sqs.' + self.region + '.amazonaws.com/' +
            self.account_id + '/' + self.get_queue_name()
        )

    def delete_message(self, message):
        self.sqs_client.delete_message(
            QueueUrl=self.get_queue_url(),
            ReceiptHandle=message.get_receipt_handle(),
        )

    def create_queue(self, queue_name):
        self.sqs_client.create_queue(
            QueueName=queue_name,
            Attributes={
                'ReceiveMessageWaitTimeSeconds': '20',
            }
        )

    def receive_message(self):
        while True:
            try:
                result = self.sqs_client.receive_message(
                    QueueUrl=self.get_queue_url(),
                    MaxNumberOfMessages=1,
                    WaitTimeSeconds=20,
                )
                if 'Messages' in result:
                    data = result['Messages'][0]
                    message = QueueMessage(data['MessageId'], json.loads(data['Body']))
                    message.set_receipt_handle(data['ReceiptHandle'])
                    break;
            except self.sqs_client.exceptions.QueueDoesNotExist as e:
                self.create_queue(self.get_queue_name())
        return message
