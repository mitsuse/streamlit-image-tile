from __future__ import annotations

from typing import Callable
from typing import Optional
from typing import Tuple
from typing import TypedDict

import streamlit as st

from PIL.Image import Image
from PIL.Image import new as new_image
from PIL.Image import open as open_image
from PIL.ImageDraw import Draw


_DEBUG = False
_impl: Optional[Tuple[Callable, Callable[[str], str]]] = None


class Content(TypedDict):
    image: Image | str
    caption: Optional[str]
    right: Optional[Right]


class Right(TypedDict):
    creator: Creator
    publisher: Publisher
    origin: str


class Creator(TypedDict):
    name: str
    url: str


class Publisher(TypedDict):
    name: str
    url: str


def captioned_image(
    content: Content,
    size: Tuple[int, int],
    key: Optional[str] = None,
) -> None:
    from os import path
    from uuid import uuid4

    import streamlit as st

    from streamlit.components import v1 as components
    from streamlit.elements.image import image_to_url

    global _impl

    if _impl is None:
        if _DEBUG:
            option_address = st.get_option("browser.serverAddress")
            option_port = st.get_option("browser.serverPort")
            _impl = (
                components.declare_component(
                    "image_tile.captioned_image",
                    url="http://localhost:3001",
                ),
                lambda s: f"http://{option_address}:{option_port}" + s,
            )
        else:
            _impl = (
                components.declare_component(
                    "image_tile.captioned_image",
                    path=path.join(
                        path.dirname(path.abspath(__file__)), "frontend/build"
                    ),
                ),
                lambda s: s,
            )

    component, build_url = _impl

    image = content["image"]
    image_square = __thumbnail(open_image(image) if image is str else image, size=size)
    width, height = size

    url_image = build_url(
        image_to_url(
            image_square,
            width=width,
            clamp=False,
            channels="RGB",
            output_format="auto",
            image_id=uuid4(),
        )
    )

    result = component(
        image=url_image,
        width=width,
        height=height,
        right=content["right"],
        caption=content["caption"],
        key=key,
        default=None,
    )


def tile(
    seq_content: Sequence[Content],
    columns: int,
    size: Tuple[int, int],
    key: str,
) -> None:
    seq_columns = st.columns(columns)

    for index, content in enumerate(seq_content):
        with seq_columns[index % columns]:
            captioned_image(content, size=size, key=f"{key}-{index}")


def __thumbnail(image: Image, size: int) -> Image:
    square = new_image("RGB", size)
    thumbnail = image.copy()
    thumbnail.thumbnail(size=size)
    w, h = size
    w_t, h_t = thumbnail.size
    square.paste(thumbnail, (int((w - w_t) / 2), int((h - h_t) / 2)))
    return square
