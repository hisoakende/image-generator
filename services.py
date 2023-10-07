import uuid
from io import BytesIO

import config
import queries
from database import execute_query
from message_queue import message_queue
from models import Event, URL, RawImage
from object_storage import object_storage
from utils import get_datetime_for_db, create_image_relative_path


def set_event(event: Event) -> None:
    execute_query(
        queries.SET_EVENT,
        {
            '$uuid': str(event.uuid),
            '$name': event.name,
            '$created_at': get_datetime_for_db(event.created_at)
        }
    )


def set_url(url: URL) -> None:
    execute_query(
        queries.SET_URL,
        {
            '$uuid': str(url.uuid),
            '$url': url.url,
            '$created_at': get_datetime_for_db(url.created_at)
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


def create_generation_image_task(raw_image_relative_path: str) -> None:
    message_queue.send_message(
        QueueUrl=config.MQ_QUERY_ENDPOINT_URL,
        MessageBody=raw_image_relative_path
    )


def get_raw_image_data(image_relative_path) -> bytes:
    response = object_storage.get_object(
        Bucket=config.OS_RAW_BUCKET_NAME,
        Key=image_relative_path
    )
    return response['Body'].read()


def generate_image(row_image_data: bytes) -> bytes:
    return row_image_data


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
