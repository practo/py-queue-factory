import urllib.parse as url_parse

from . import Sqs

class SqsLocal(Sqs):
    def __init__(self, uri, host_url, subdomain):
        client_kwargs = {
            'use_ssl': False,
            'verify': False
        }
        parts = url_parse.urlparse(uri)
        host_parts = parts.hostname.split('.', 2)
        endpoint_url = parts.scheme + '://' + host_parts[2] + ':' + str(parts.port)
        super(SqsLocal, self).__init__(uri, host_url, subdomain, endpoint_url, client_kwargs)

    def get_queue_url(self):
        queue_url = self.sqs_client.get_queue_url(QueueName=self.get_queue_name())['QueueUrl']

        return queue_url.replace('localhost', 'awslocal')
