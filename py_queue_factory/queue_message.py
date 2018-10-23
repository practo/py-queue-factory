class QueueMessage:
    def __init__(self, message_id, message_body):
        self._id = message_id
        self._body = message_body

    def get_body(self):
        return self._body

    def get_id(self):
        return self._id

    def get_receipt_handle(self):
        return self._receipt_handle

    def set_receipt_handle(self, receipt_handle):
        self._receipt_handle = receipt_handle
