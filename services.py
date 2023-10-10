import base64
import json
import uuid
from io import BytesIO

import requests

import config
import queries
from database import execute_query
from message_queue import message_queue
from models import Event, RawImage, Domain
from object_storage import object_storage
from utils import get_datetime_for_db, create_image_relative_path, get_generation_args


def set_event(event: Event) -> None:
    execute_query(
        queries.SET_EVENT,
        {
            '$uuid': str(event.uuid),
            '$name': event.name,
            '$created_at': get_datetime_for_db(event.created_at)
        }
    )


def set_domain(domain: Domain) -> None:
    execute_query(
        queries.SET_DOMAIN,
        {
            '$uuid': str(domain.uuid),
            '$domain': domain.domain,
            '$created_at': get_datetime_for_db(domain.created_at)
        }
    )


def save_raw_image(raw_image: RawImage) -> str:
    event_uuid = get_current_event_uuid()
    image_relative_path = create_image_relative_path(raw_image, event_uuid)
    object_storage.upload_fileobj(
        Fileobj=BytesIO(raw_image.image_data),
        Bucket=config.OS_RAW_BUCKET_NAME,
        Key=image_relative_path
    )
    return image_relative_path


def create_generation_image_task(raw_image: RawImage, image_relative_path: str) -> None:
    generation_args = get_generation_args(raw_image, image_relative_path)
    message_queue.send_message(
        QueueUrl=config.MQ_QUERY_ENDPOINT_URL,
        MessageBody=json.dumps(generation_args)
    )


def get_raw_image_data(image_relative_path: str) -> bytes:
    response = object_storage.get_object(
        Bucket=config.OS_RAW_BUCKET_NAME,
        Key=image_relative_path
    )
    return response['Body'].read()


def generate_image(raw_image_data: bytes,
                   generation_args: dict[str, str | int | float]) -> bytes:
    domain = get_current_domain()
    raw_image_base64 = base64.b64encode(raw_image_data).decode()
    generation_args['init_images'] = [raw_image_base64]
    response = requests.post(domain, json=generation_args)
    return base64.b64decode(response.json()['images'][0])


def save_generated_image(generated_image_data: bytes, image_relative_path: str) -> None:
    object_storage.upload_fileobj(
        BytesIO(generated_image_data),
        config.OS_GENERATED_BUCKET_NAME,
        image_relative_path
    )


def get_current_event_uuid() -> uuid.UUID:
    response = execute_query(
        queries.GET_CURRENT_EVENT_UUID,
        {}
    )
    return uuid.UUID(response[0].rows[0]['uuid'].decode())


def get_current_domain() -> str:
    response = execute_query(
        queries.GET_CURRENT_DOMAIN,
        {}
    )
    domain = response[0].rows[0]['domain'].decode()
    return 'https://' + domain + config.IMAGE_GENERATION_RELATIVE_ENDPOINT
