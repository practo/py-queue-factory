import urllib.parse as url_parse

from . import Sqs, SqsLocal

class QueueFactory:
    @staticmethod
    def get_queue(queue_uri, host_url, subdomain):
        parts = url_parse.urlparse(queue_uri)
        if parts.scheme == 'https':
            host = parts.hostname
            host_parts = host.split('.', 2)
            if host_parts[0] == 'sqs' and host_parts[2] == 'amazonaws.com':
                return Sqs(queue_uri, host_url, subdomain)
            elif host_parts[0] == 'sqs' and host_parts[2] == 'awslocal':
                return SqsLocal(queue_uri, host_url, subdomain)
            else:
                raise Exception('Invalid Sqs URI')
        else:
            raise Exception('Unsupported URI scheme')
