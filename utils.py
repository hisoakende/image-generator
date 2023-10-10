import imghdr
import json
import uuid
from copy import deepcopy
from datetime import datetime
from typing import Any, Callable

import pytz

import config
import responses
from exceptions import ValidationError


def get_current_datetime() -> datetime:
    return datetime.now(pytz.timezone(config.TIMEZONE))


def get_datetime_for_db(datetime_: datetime) -> str:
    return datetime_.astimezone(pytz.timezone('UTC')).strftime('%Y-%m-%dT%H:%M:%SZ')


def get_successful_response(body: dict[str, Any] | None = None) -> dict[str, Any]:
    response = deepcopy(responses.SUCCESSFUL_RESPONSE)
    if body is not None:
        response['body'] = body
    return response


def create_filename(data: bytes) -> str:
    uuid_ = uuid.uuid4()
    extension = imghdr.what(None, data)
    if extension is None:
        raise ValidationError
    return f'{uuid_}.{extension}'


def create_image_relative_path(image: 'Image', event_uuid: uuid.UUID) -> str:
    return f'{event_uuid}/{image.name}'


def get_generation_args(raw_image: 'RawImage',
                        image_relative_path: str) -> dict[str, str | int | float]:
    generation_args = {k: v for k, v in vars(raw_image).items() if k not in ('image_data', 'name')}
    return generation_args | {'image_relative_path': image_relative_path}


def create_generated_image_absolute_path(relative_path: str) -> str:
    return f'{config.OS_ENDPOINT_URL}/{config.OS_GENERATED_BUCKET_NAME}/{relative_path}'


def process_model_from_request(model_class: type['Model']) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(request: dict, context: 'RuntimeContext') -> dict[str, Any]:
            body = _get_body(request)
            try:
                model = model_class(**body)
            except ValidationError:
                return responses.INVALID_DATA
            return func(request, context, model)

        return wrapper

    return decorator


def process_data_from_trigger(func: Callable) -> Callable:
    def wrapper(event: dict[str, Any], context: 'RuntimeContext') -> dict[str, Any]:
        body = event['messages'][0]['details']['message']['body']
        return func(event, context, json.loads(body))

    return wrapper


def authorization_by_code(func: Callable) -> Callable:
    def wrapper(request: dict[str, Any], context: 'RuntimeContext') -> dict[str, Any]:
        code = request['queryStringParameters'].get('code')
        if code is None or code != config.AUTHORIZATION_CODE:
            return responses.PERMISSION_DENIED
        return func(request, context)

    return wrapper


def _get_body(request: dict) -> dict[str, Any]:
    return json.loads(request['body'])
