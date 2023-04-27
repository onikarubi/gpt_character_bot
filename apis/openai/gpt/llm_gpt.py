from abc import ABCMeta, abstractmethod
from dotenv import load_dotenv
from typing import Union
from logs.request_logger import logger_output
import openai
import os

load_dotenv()

class GPT3Model(metaclass=ABCMeta):
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    def __init__(
        self,
        model: str,
        supported_models: list[str] = None,
        max_tokens: int = 100,
        temperature: float = 0,
        top_p: float = 0
    ) -> None:
        self._use_model = model
        self.supported_models = supported_models
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        openai.api_key = self.OPENAI_API_KEY

    @property
    def use_model(self):
        if not self._use_model or not self._use_model in self.supported_models:
            raise ValueError('対応しているモデルはありません')

        return self._use_model

    @abstractmethod
    def create_completion(self, prompt: Union[str, dict[str, any]]) -> str:
        """Generate a completion for the given prompt."""
        pass


class GPT3ChatCompletion(GPT3Model):
    CHAT_COMPLETION_SUPPORTED_MODELS = ['gpt-3.5-turbo', "gpt-3.5-turbo-0301"]

    def __init__(self, model: str, supported_models: list[str] = None, max_tokens: int = 100, temperature: float = 0, top_p: float = 0) -> None:
        super().__init__(model, supported_models, max_tokens, temperature, top_p)
        self.supported_models = self.CHAT_COMPLETION_SUPPORTED_MODELS

    def create_completion(self, messages: Union[str, dict[str, any]]) -> str:
        try:
            completion = openai.ChatCompletion.create(
                model=self.use_model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p
            )
            response_content = completion.choices[0].message.content.replace('\n', '')

            logger_output(level='info', message='応答メッセージの生成に成功しました', output_filename='openai_access')
            return response_content

        except:
            raise


