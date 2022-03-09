import boto3
import urllib.parse as url_parse

from . import AbstractQueue, QueueMessage


class Sqs(AbstractQueue):
    RECEIVE_MESSAGE_WAIT_TIME = '20'
    RECEIVE_MAX_NUMBER_OF_MESSAGES = 1
    SQS_MAX_VISIBILITY_TIMEOUT = 60 * 60 * 12  # 12 hrs

    def __init__(self, uri, host_url, subdomain, endpoint_url=None,
                 client_kwargs={}):
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

    def do_send_message(self, message, delay, attempt=1):
        if delay > 900:
            delay = 900
        try:
            message_body = AbstractQueue.encode_mesage(message.get_body(), self.encoding)
            respone = self.sqs_client.send_message(
                QueueUrl=self.get_queue_url(),
                MessageBody=message_body,
                DelaySeconds=delay,
            )
            message.set_id(respone['MessageId'])
        except self.sqs_client.exceptions.QueueDoesNotExist as e:
            self.create_queue(self.get_queue_name())
            if attempt < 3:
                attempt += 1
                self.do_send_message(message, delay, attempt)
            else:
                raise Exception('Could not send message')

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
                'ReceiveMessageWaitTimeSeconds': str(self.RECEIVE_MESSAGE_WAIT_TIME),
                'VisibilityTimeout': str(self.visibility_timeout),
            }
        )

    def receive_message(self, attribute_names=[]):
        while True:
            try:
                result = self.sqs_client.receive_message(
                    QueueUrl=self.get_queue_url(),
                    AttributeNames=attribute_names,
                    MaxNumberOfMessages=self.RECEIVE_MAX_NUMBER_OF_MESSAGES,
                    WaitTimeSeconds=int(self.RECEIVE_MESSAGE_WAIT_TIME),
                    VisibilityTimeout=int(self.visibility_timeout),
                )
                if 'Messages' in result:
                    data = result['Messages'][0]
                    message_body = AbstractQueue.decode_message(data['Body'], self.encoding)
                    message = QueueMessage(message_body, data['MessageId'])
                    message.set_receipt_handle(data['ReceiptHandle'])
                    message.set_attributes(data.get('Attributes', {}))
                    break
            except self.sqs_client.exceptions.QueueDoesNotExist as e:
                self.create_queue(self.get_queue_name())
        return message

    def change_message_visibility(self, message, visibility_timeout):
        if visibility_timeout > self.SQS_MAX_VISIBILITY_TIMEOUT:
            visibility_timeout = self.SQS_MAX_VISIBILITY_TIMEOUT

        self.sqs_client.change_message_visibility(
            QueueUrl=self.get_queue_url(),
            ReceiptHandle=message.get_receipt_handle(),
            VisibilityTimeout=visibility_timeout
        )

    def validate_visibility_timeout(self):
        if self.visibility_timeout > self.SQS_MAX_VISIBILITY_TIMEOUT:
            raise Exception(f'visibility_timeout range 0 to '
                            f'{self.SQS_MAX_VISIBILITY_TIMEOUT}, but received'
                            f' {self.visibility_timeout}')
