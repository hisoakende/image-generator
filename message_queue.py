import boto3

import config

message_queue = None

if config.USE_MS:
    message_queue = boto3.client(
        'sqs',
        aws_access_key_id=config.STATIC_KEY_ID,
        aws_secret_access_key=config.STATIC_KEY,
        region_name=config.REGION_NAME,
        endpoint_url=config.MQ_ENDPOINT_URL
    )
