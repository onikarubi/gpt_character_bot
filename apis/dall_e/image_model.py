from openai import Image
import os
import openai

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    from dotenv import load_dotenv
    load_dotenv('./.env')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

class ImageUrlNotFoundException(Exception):
    pass


class ImageSize:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y
        self._image_size = f"{self.x}x{self.y}"
        self.image_size_list = ['256x256', '512x512', '1024x1024']

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def image_size(self):
        if not self._image_size in self.image_size_list:
            return

        return self._image_size


class ImageModel:
    DEFAULT_OUTPUT = 'output/output.png'

    def __init__(self, image_size: ImageSize, output_image: str = DEFAULT_OUTPUT, input_image: str = None) -> None:
        self._image_size = image_size.image_size

        if not output_image.split('.')[-1] == "png":
            raise ValueError

        self._output_image = output_image

        if input_image:
            self._input_image = input_image

    @property
    def image_size(self): return self._image_size

    @property
    def output_image(self): return self._output_image

    @property
    def input_image(self):
        if not self._input_image:
            return

        return self._input_image

    @input_image.setter
    def set_input_image(self, image_name: str):
        if not image_name.split(".")[-1] == "png":
            raise ValueError

        self._input_image = image_name


class ImageGenerator(ImageModel):
    DEFAULT_OUTPUT = 'output/output.png'

    def __init__(self, image_size: ImageSize, output_image: str = DEFAULT_OUTPUT, input_image: str = None, prompt: str = '') -> None:
        super().__init__(image_size, output_image, input_image)
        self._prompt = prompt

    def create_image(self, n: int = 1):
        response = Image.create(
            prompt=self._prompt,
            n=n,
            size=self.image_size
        )

        response_url = response['data'][0]['url']
        if not response_url:
            raise ImageUrlNotFoundException('This url is not found.')

        print('Image generation is complete!!')

        return response_url

    def recreate_image(self, n: int = 1):
        response = Image.create_variation(
            image=open(self.input_image, "rb"),
            n=n,
            size=self.image_size
        )
        response_url = response['data'][0]['url']
        if not response_url:
            raise ImageUrlNotFoundException('This url is not found.')

        print('Image generation is complete!!')

        return response_url
