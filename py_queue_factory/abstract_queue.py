import urllib.parse as url_parse

class AbstractQueue:
    """
    Queue name on staging or latest will get suffixed with stag name / latest
    Also it will have a prefix as mentioned in the queue uri
    Ex: prod-subscriptions-
    """
    def set_host_url(self, host_url):
        self.host_url = host_url

        return self

    def set_subdomain(self, subdomain):
        self.subdomain = subdomain

        return self

    def set_queue_name(self, queue_name):
        self.queue_name = queue_name

        return self

    def get_queue_name(self):
        """suffixing latest/staging name to queue name"""
        parts = url_parse.urlparse(self.host_url)
        subdomain = parts.hostname.split('.')[0]
        queue_name_with_suffix = subdomain.replace(self.subdomain, self.queue_name)

        return self.queue_prefix + queue_name_with_suffix
