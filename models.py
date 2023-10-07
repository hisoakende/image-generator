import uuid
from typing import Any

from utils import get_current_datetime, create_filename
from validators import validate_base64_image


class Model:
    pass


class UUIDFieldMixin:

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.uuid = uuid.uuid4()


class CreatedAtFieldMixin:

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.created_at = get_current_datetime()


class Event(Model, UUIDFieldMixin, CreatedAtFieldMixin):

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name


class URL(Model, UUIDFieldMixin, CreatedAtFieldMixin):

    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url


class RawImage(Model):

    def __init__(self, image: str) -> None:
        self.image_data = validate_base64_image(image)
        self.name = create_filename(self.image_data)
