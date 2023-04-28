from pydantic import BaseModel


class ImageData(BaseModel):
    text: str
    vertical_padding: int
    horizontal_padding: int
    image_color: str
    text_color: str
    width: int
    height: int
