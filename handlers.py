from typing import Any

import services
from models import Event, Domain, RawImage
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
@process_model_from_request(Domain)
def set_url(request: dict[str, Any],
            context: 'RuntimeContext',
            domain: Domain) -> dict[str, Any]:
    services.set_domain(domain)
    return get_successful_response(vars(domain))


@process_model_from_request(RawImage)
def accept_image(request: dict[str, Any],
                 context: 'RuntimeContext',
                 raw_image: RawImage) -> dict[str, Any]:
    image_relative_path = services.save_raw_image(raw_image)
    services.create_generation_image_task(raw_image, image_relative_path)
    return get_successful_response({
        'image': create_generated_image_absolute_path(image_relative_path)
    })


@process_data_from_trigger
def generate_image(event: dict[str, Any],
                   context: 'RuntimeContext',
                   generation_args: dict[str, str | int | float]) -> None:
    image_relative_path = generation_args.pop('image_relative_path')
    raw_image_data = services.get_raw_image_data(image_relative_path)
    generated_image_data = services.generate_image(raw_image_data, generation_args)
    services.save_generated_image(generated_image_data, image_relative_path)
