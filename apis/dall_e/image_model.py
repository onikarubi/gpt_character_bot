from openai import Image
from .initialize import open_ai_init

open_ai_init()

class ImageUrlNotFoundException(Exception):
    pass

class ImageSize:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y
        self._size = f"{self.x}x{self.y}"
        self.image_size_list = ['256x256', '512x512', '1024x1024']

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def size(self):
        if not self._size in self.image_size_list:
            raise ValueError('特定のサイズが含まれていない')

        return self._size


class ImageModel:
    DEFAULT_OUTPUT = 'output/output.png'

    def __init__(self, image_size: ImageSize, output_image: str = DEFAULT_OUTPUT, input_image: str = None) -> None:
        self._image_size = image_size.size

        if not output_image.split('.')[-1] == "png":
            raise ValueError

        self._output_image = output_image

        if input_image:
            self._input_image = input_image

    @property
    def image_size(self): return self._image_size

    @property
    def output_image(self): return self._output_image

    @output_image.setter
    def set_output_image(self, image: str):
        if image:
            if image.split(".")[-1] == "png":
                self.output_image = image
                return

        raise ValueError('正しいURLが指定されていません')

    @property
    def input_image(self):
        if not self._input_image:
            return

        return self._input_image

    @input_image.setter
    def set_input_image(self, image: str):
        if image:
            if image.split(".")[-1] == "png":
                self.input_image = image
                return

        raise ValueError('正しいURLが指定されていません')


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

        response_url = self._get_response_url(response)

        return response_url

    def recreate_image(self, n: int = 1):
        response = Image.create_variation(
            image=open(self.input_image, "rb"),
            n=n,
            size=self.image_size
        )
        response_url = self._get_response_url(response)

        print('Image generation is complete!!')

        return response_url

    def _get_response_url(self, response):
        response_url = response['data'][0]['url']
        if not response_url:
            raise ImageUrlNotFoundException('This url is not found.')
