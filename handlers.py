from typing import Any

import services
from models import Event, URL, RawImage
from utils import (
    get_successful_response, create_generated_image_absolute_path,
    process_model_from_request, process_data_from_trigger, authorization_by_code
)


@authorization_by_code
@process_model_from_request(Event)
def set_event(request: dict[str, Any],
              context: 'RuntimeContext',
              event: Event) -> dict[str, Any]:
    services.set_event(event)
    return get_successful_response(vars(event))


@authorization_by_code
@process_model_from_request(URL)
def set_url(request: dict[str, Any],
            context: 'RuntimeContext',
            url: URL) -> dict[str, Any]:
    services.set_url(url)
    return get_successful_response(vars(url))


@process_model_from_request(RawImage)
def accept_image(request: dict[str, Any],
                 context: 'RuntimeContext',
                 raw_image: RawImage) -> dict[str, Any]:
    image_relative_path = services.save_raw_image(raw_image)
    services.create_generation_image_task(image_relative_path)
    return get_successful_response({
        'image': create_generated_image_absolute_path(image_relative_path)
    })


@process_data_from_trigger
def generate_image(event: dict[str, Any],
                   context: 'RuntimeContext',
                   image_relative_path: str) -> dict[str, Any]:
    row_image_data = services.get_raw_image_data(image_relative_path)
    generated_image_data = services.generate_image(row_image_data)
    services.save_generated_image(generated_image_data, image_relative_path)
