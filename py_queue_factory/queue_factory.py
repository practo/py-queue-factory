import urllib.parse as url_parse

from . import Sqs, SqsLocal, Beanstalk


class QueueFactory:
    @staticmethod
    def get_queue(queue_uri, host_url, subdomain, port=None):
        parts = url_parse.urlparse(queue_uri)
        host = parts.hostname
        host_parts = host.split('.', 2)
        if parts.scheme == 'https':
            if host_parts[0] == 'sqs' and host_parts[2] == 'amazonaws.com':
                return Sqs(queue_uri, host_url, subdomain)
            elif host_parts[0] == 'sqs' and host_parts[2] == 'awslocal':
                return SqsLocal(queue_uri, host_url, subdomain)
            else:
                raise Exception('Invalid Sqs URI')
        elif parts.scheme == 'beanstalk':
            if host_parts[0] == 'beanstalkd':
                return Beanstalk(queue_uri, host_url, subdomain, port) \
                    if port else Beanstalk(queue_uri, host_url, subdomain)
            else:
                raise Exception('Invalid Beanstalk URI')
        else:
            raise Exception('Unsupported URI scheme')
