class QueueMessage:
    def __init__(self, message_body, message_id=None):
        self._body = message_body
        self._id = message_id

    def get_body(self):
        return self._body

    def set_id(self, id):
        self._id = id
        return self

    def get_id(self):
        return self._id

    def get_receipt_handle(self):
        return self._receipt_handle

    def set_receipt_handle(self, receipt_handle):
        self._receipt_handle = receipt_handle
        return self
