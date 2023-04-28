import io

from PIL import (
    Image as ImagePackage,
    ImageFont,
    ImageColor as ImageColorPackage,
    ImageDraw as ImageDrawPackage
)
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw


RGB_MODE = "RGB"


class TextPainter:
    def __init__(self):
        self.mode = RGB_MODE
        self.font = ImageFont.load_default()

    def _get_color(self, color: str) -> tuple[int, int, int]:
        try:
            return ImageColorPackage.getcolor(
                color=color,
                mode=self.mode,
            )
        except ValueError:
            msg = "Color does not exists"
            raise ValueError(msg)

    def _create_image(
        self,
        width: int,
        height: int,
        color: tuple,
    ) -> Image:
        return ImagePackage.new(
            mode=self.mode,
            size=(width, height),
            color=color,
        )

    def _create_draw(self, image) -> ImageDraw:
        return ImageDrawPackage.Draw(
            im=image,
            mode=self.mode,
        )

    def _get_font_height(self, text: str) -> int:
        _, _, _, font_height = self.font.getbbox(text)
        return font_height

    def _create_sentence_by_words(self, words: list[str]) -> str:
        return " ".join(words)

    def _check_image_size(self, line_height: int, max_line_height: int):
        if line_height > max_line_height:
            msg = "Too long text for this image size and paddings"
            raise ValueError(msg)

    def create_image(
        self,
        text: str,
        vertical_padding: int = 10,
        horizontal_padding: int = 10,
        image_color: str = "white",
        text_color: str = "black",
        width: int = 256,
        height: int = 256,
    ) -> Image:
        font_height = self._get_font_height(text)
        text_color_rgb = self._get_color(text_color)
        image_color_rgb = self._get_color(image_color)
        image = self._create_image(width, height, image_color_rgb)
        draw = self._create_draw(image)
        line_height = vertical_padding
        max_line_height = image.height - (font_height + vertical_padding)

        words = text.split()
        while words:
            string_words = []
            while True:
                string = self._create_sentence_by_words(string_words)
                if not words:
                    self._check_image_size(line_height, max_line_height)
                    draw.text(
                        xy=(horizontal_padding, line_height),
                        text=string,
                        fill=text_color_rgb,
                        font=self.font,
                    )
                    break
                if draw.textlength(
                    text=string + words[0],
                    font=self.font
                ) > image.width - horizontal_padding * 2:
                    self._check_image_size(line_height, max_line_height)
                    draw.text(
                        xy=(horizontal_padding, line_height),
                        text=string,
                        fill=text_color_rgb,
                        font=self.font,
                    )
                    line_height += font_height
                    break
                string_words.append(words.pop(0))

        return image

    @staticmethod
    def get_image_bytes(image: Image) -> bytes:
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()
        return image_bytes
