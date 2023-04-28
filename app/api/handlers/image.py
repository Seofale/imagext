from fastapi import Depends, APIRouter, Response

from app.painters.text_painter import TextPainter
from app.api.schemas.image import ImageData


router = APIRouter()


@router.post(
    "/create-image/",
    responses={
        200: {
            "content": {"image/png": {}}
        },
    },
)
def create_text_image(
    image_data: ImageData,
    text_painter: TextPainter = Depends(TextPainter),
):
    image = text_painter.create_image(**image_data.dict())
    return Response(
        content=text_painter.get_image_bytes(image),
        status_code=200,
        media_type="image/png",
    )
