from py_queue_factory import QueueFactory

ACCOUNTS_SIGNUP_QUEUE = {
    'name': 'accounts-signup',
    'visibility_timeout': 100,  # in secs, default 60 secs
    'encoding': 'json',  # default base64
}

queue = QueueFactory.get_queue(
    'https://<aws_access_key>:<aws_secret_key>@sqs.<region>.amazonaws.com/<account_id>/<queue_prefix>'
    'https://subscriptions-stag.practodev.com',
    'subscriptions'
)

payload_to_send = {'test': 'some data'}
print('Sending message')
queue \
    .set_queue_properties(ACCOUNTS_SIGNUP_QUEUE) \
    .send_message(payload_to_send, delay=5)
# delay is optinal, default is 0
print('Message sent')

print('Receiving message')
message = queue \
    .set_queue_properties(ACCOUNTS_SIGNUP_QUEUE) \
    .receive_message()
print('Message received')

payload = message.get_body()
print(payload['test'])  # prints some data

print('Deleting message')
queue \
    .set_queue_properties(ACCOUNTS_SIGNUP_QUEUE) \
    .delete_message(message)
print('Message deleted')

# Note: Multiple calls to set_queue_properties not needed if not dealing
# with multiple queues in the samw worker
