from fastapi import (APIRouter, Depends, File, Form, Response, UploadFile,
                     status)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pydantic import ValidationError

from app.api.schemas.image import ImageData, ImageDataWithBackColor
from app.painters.text_painter import TextPainter

router = APIRouter()


def get_image_data(image_data: str = Form(...)):
    try:
        image_data = ImageData.parse_raw(image_data)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return image_data


@router.post(
    "/create-image-background/",
    responses={
        200: {
            "content": {"image/png": {}}
        },
    },
)
def create_image_with_background(
    image_data: ImageData = Depends(get_image_data),
    image_background: UploadFile = File(...),
    text_painter: TextPainter = Depends(),
) -> Response:
    content = image_background.file.read()
    image = text_painter.create_image(
        **image_data.dict(),
        background=content,
    )
    return Response(
        content=text_painter.get_image_bytes(image),
        status_code=200,
        media_type="image/png",
    )


@router.post("/create-image/")
def create_image(
    image_data: ImageDataWithBackColor,
    text_painter: TextPainter = Depends(),
) -> Response:
    image = text_painter.create_image(
        **image_data.dict(),
    )
    return Response(
        content=text_painter.get_image_bytes(image),
        status_code=200,
        media_type="image/png",
    )
