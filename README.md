# Python Queue Factory
py-queue-factory is a python library that takes care of creating required queue instances so that you only have to worry about actually using the queue

## Quick Links
* [Installation](https://github.com/practo/py-queue-factory#installation)
* [Usage](https://github.com/practo/py-queue-factory#usage)
* [Features](https://github.com/practo/py-queue-factory#features)
* [Queue URI Examples](https://github.com/practo/py-queue-factory#queue-uri-examples)
* [Debugging](https://github.com/practo/py-queue-factory#debugging)

## Installation
```python
pip install git+https://github.com/practo/py-queue-factory.git@<commit_hash/version>
```

## Usage
Params required `queue_uri`, `host_url` and `subdomain`  
`queue_uri` is used to decide what type of queue to create (SQS, SQS Local, Beanstalk)  
`host_url` and `subdomain` is used to decide the actual queue name (staging name/latest is suffixed to queue name)  

If queue prefix is `prod-subscriptions-`  
queue name is `random-queue`  
and host url is `https://subscriptions-stag.practodev.com`  
actual queue name would be `prod-subscriptions-random-queue-stag`  
```python
from py_queue_factory import QueueFactory

queue = QueueFactory.get_queue(queue_uri, host_url, subdomain)

# To receive message
message = queue\
    .set_queue_name('my-queue-name')\
    .receive_message()

# To delete message
queue\
    .set_queue_name('my-queue-name')\
    .delete_message(message)
```

## Features
#### SQS
- [ ] Send Message
- [x] Receive Message
- [x] Delete Message
- [x] Create queue if not exists
#### SQS Local
- [ ] Send Message
- [x] Receive Message
- [x] Delete Message
- [x] Create queue if not exists
#### Beanstalk
- [ ] Send Message
- [ ] Receive Message
- [ ] Delete Message
- [ ] Create queue if not exists

## Queue URI Examples:
```python
# Format for AWS SQS queue
QUEUE_URI = 'https://<aws_access_key>:<aws_secret_key>@sqs.<region>.amazonaws.com/<account_id>/<queue_prefix>'

# Format for AWSLocal/localstack SQS queue
QUEUE_URI = 'https://anything:anything@sqs.<region>.awslocal:<sqs_port>/<account_id>/<queue_prefix>'

#Example AWS local SQS queue uri
QUEUE_URI = 'https://anything:anything@sqs.ap-south-east-1.awslocal:4576/1/prod-subscriptions-'

#Example AWS SQS queue uri
QUEUE_URI = 'https://AKIAJHY5ABCPXF4YXXYZ:kdsjhfkjsdksdfkdsjnckjsdnkfjdsdkfjndskjf@sqs.ap-south-1.amazonaws.com/961234512345/prod-subscriptions-'
```

## Debugging
For debugging you can clone this repo locally and install it from that location
```python
pip install -e <location of py_queue_factory>
```
Note: Remove any previously installed version of this library
