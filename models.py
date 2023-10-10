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


class Domain(Model, UUIDFieldMixin, CreatedAtFieldMixin):

    def __init__(self, domain: str) -> None:
        super().__init__()
        self.domain = domain


class RawImage(Model):

    def __init__(self,
                 text: str,
                 mask_blur: int,
                 steps: int,
                 denoising_strength: float,
                 cfg_scale: int,
                 width: int,
                 height: int,
                 webImg64: str) -> None:
        self.promt = text
        self.mask_blur = mask_blur
        self.steps = steps
        self.denoising_strength = denoising_strength
        self.cfg_scale = cfg_scale
        self.width = width
        self.height = height
        self.image_data = validate_base64_image(webImg64)
        self.name = create_filename(self.image_data)
