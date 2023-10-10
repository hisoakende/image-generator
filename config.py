import os

TIMEZONE = 'Europe/Moscow'

USE_YDB = int(os.getenv('USE_YDB', 0))
USE_OS = int(os.getenv('USE_OS', 0))
USE_MS = int(os.getenv('USE_OS', 0))

AUTHORIZATION_CODE = os.getenv('AUTHORIZATION_CODE')

STATIC_KEY = os.getenv('STATIC_KEY')
STATIC_KEY_ID = os.getenv('STATIC_KEY_ID')
REGION_NAME = 'ru-central1'

YDB_DATABASE = os.getenv('YDB_DATABASE')
YDB_ENDPOINT = os.getenv('YDB_ENDPOINT')
YDB_EVENT_TABLE = 'event'
YDB_DOMAIN_TABLE = 'domain'

OS_ENDPOINT_URL = 'https://storage.yandexcloud.net'
OS_RAW_BUCKET_NAME = 'sd-rawstorage'
OS_GENERATED_BUCKET_NAME = 'sd-generatedstorage'

MQ_ENDPOINT_URL = os.getenv('MQ_ENDPOINT_URL')
MQ_QUERY_ENDPOINT_URL = os.getenv('MQ_QUERY_ENDPOINT_URL')

IMAGE_GENERATION_RELATIVE_ENDPOINT = '/sdapi/v1/img2img'
