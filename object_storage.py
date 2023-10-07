import boto3

import config

object_storage = None

if config.USE_OS:
    object_storage = boto3.client(
        's3',
        aws_access_key_id=config.STATIC_KEY_ID,
        aws_secret_access_key=config.STATIC_KEY,
        region_name=config.REGION_NAME,
        endpoint_url=config.OS_ENDPOINT_URL
    )
