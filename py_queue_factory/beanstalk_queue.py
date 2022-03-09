import urllib.parse as url_parse

import beanstalkc3
from beanstalkc3 import Job

from . import AbstractQueue, QueueMessage


class Beanstalk(AbstractQueue):

    BEANSTALK_MAX_VISIBILITY_TIMEOUT = 60 * 60 * 12  # 12 hours
    BEANSTALK_RECEIVE_MESSAGE_WAIT_TIME = 30  # 30 seconds

    def __init__(self, uri, host_url, subdomain, default_port=11300):
        parts = url_parse.urlparse(uri)
        host = parts.hostname
        self.scheme = parts.scheme
        port = parts.port if parts.port else default_port
        self.set_host_url(host_url).set_subdomain(subdomain)
        path_parts = list(filter(None, parts.path.split('/')))
        self.queue_prefix = "/".join(path_parts) if path_parts else ''
        self.beanstalk_client = beanstalkc3.Connection(host=host, port=port)

    def do_send_message(self, message, delay, attempt=1):
        if delay > 900:
            delay = 900
        try:
            message_body = AbstractQueue.encode_mesage(message.get_body(), self.encoding)
            self.beanstalk_client.use(self.get_queue_url())
            respone = self.beanstalk_client.put(message_body, delay=delay, ttr=self.visibility_timeout)
            message.set_id(respone)
        except:
            if attempt < 3:
                attempt += 1
                self.do_send_message(message, delay, attempt)
            else:
                raise Exception('Could not send message')

    def delete_message(self, message):
        job = Job(self.beanstalk_client, message.get_id(), message.get_body())
        job.delete()

    def receive_message(self):
        self.beanstalk_client.watch(self.get_queue_url())
        result = self.beanstalk_client.reserve(self.BEANSTALK_RECEIVE_MESSAGE_WAIT_TIME)
        message = QueueMessage(result.jid, AbstractQueue.decode_message(result.body, self.encoding))

        return message

    def get_queue_url(self):
        return url_parse.urljoin(self.scheme + '://', 'beanstalkd',
                                 self.get_queue_name())

    def change_message_visibility(self, message, visibility_timeout):
        pass

    def validate_visibility_timeout(self):
        if self.visibility_timeout > self.BEANSTALK_MAX_VISIBILITY_TIMEOUT:
            raise Exception(f'visibility_timeout range 0 to '
                            f'{self.BEANSTALK_MAX_VISIBILITY_TIMEOUT}, but received'
                            f' {self.visibility_timeout}')
