import copy
from abc import ABC, abstractmethod
import urllib.parse as url_parse

from .queue_message import QueueMessage


class AbstractQueue(ABC):
    """
    Queue name on staging or latest will get suffixed with stag name / latest
    Also it will have a prefix as mentioned in the queue uri
    Ex:
    prefix: prod-subscriptions-, queue name: my-queue, stag name(suffix): sub
    final queue name: prod-subscriptions-my-queue-sub
    """

    DEFAULT_VISIBILITY_TIMEOUT = 60  # 60 secs
    DEFAULT_ENCODING = 'base64'
    VALID_ENCODING = ['json', 'base64']

    def send_message(self, message, delay=0):
        if not isinstance(message, QueueMessage):
            # message = self.handle_cid(message)
            message = QueueMessage(message)
        self.do_send_message(message, delay)

    @abstractmethod
    def do_send_message(message, delay):
        pass

    @abstractmethod
    def receive_message(self):
        pass

    @abstractmethod
    def delete_message(self, message):
        pass

    @abstractmethod
    def change_message_visibility(self, message, visibility_timeout):
        pass

    @abstractmethod
    def validate_visibility_timeout(self):
        pass

    def set_host_url(self, host_url):
        self.host_url = host_url

        return self

    def set_subdomain(self, subdomain):
        self.subdomain = subdomain

        return self

    def set_queue_properties(self, queue_properties):
        queue_properties = copy.deepcopy(queue_properties)
        self.queue_name = queue_properties.pop('name')
        self.visibility_timeout = queue_properties.pop(
            'visibility_timeout', self.DEFAULT_VISIBILITY_TIMEOUT)
        self.encoding = queue_properties.pop(
            'encoding', self.DEFAULT_ENCODING)
        self.validate_queue_properties()
        if queue_properties:
            raise Exception(f'Unknown queue properties {queue_properties}')

        return self

    def validate_queue_properties(self):
        self.validate_encoding()
        self.validate_visibility_timeout()

    def validate_encoding(self):
        if not self.encoding:
            raise Exception('Encoding is not specified')
        if self.encoding not in (self.VALID_ENCODING):
            raise Exception(f'Unknown encoding type, Known types are '
                            f'{self.VALID_ENCODING} but received '
                            f'\'{self.encoding}\'')

    def get_queue_name(self):
        """suffixing latest/staging name to queue name"""
        parts = url_parse.urlparse(self.host_url)
        subdomain = parts.hostname.split('.')[0]
        queue_name_with_suffix = subdomain.replace(
            self.subdomain, self.queue_name)

        return self.queue_prefix + queue_name_with_suffix
