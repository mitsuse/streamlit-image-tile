from __future__ import annotations

from typing import Tuple

import streamlit as st
from PIL.Image import Image
from PIL.Image import open as open_image

def main() -> None:
    from image_tile import Content, Creator, Right, Publisher
    from image_tile import tile

    st.title("Image Tile")

    image = open_image("dummy.png")
    origin="https://dummyimage.com/"
    creator = Creator(name="Creator's Name", url=origin)
    publisher = Publisher(name="Publisher's Name", url=origin)
    right = Right(creator=creator, publisher=publisher, origin=origin)

    st.markdown("## Tile images with right attributions")
    seq_content=tuple(Content(image=image, caption=f"Dummy Image {x}", right=right) for x in range(6))
    tile(seq_content=seq_content, columns=4, size=(180, 216), key="with_right")

    st.markdown("## Tile images without right attributions")
    # seq_content=tuple(Content(image=image, caption=f"Dummy Image {x}", right=None) for x in range(6))
    seq_content=tuple(Content(image=image, caption=f"Dummy Image {x}", right=None if x % 2 else right) for x in range(6))
    tile(seq_content=seq_content, columns=4, size=(180, 216), key="without_right")


main()
