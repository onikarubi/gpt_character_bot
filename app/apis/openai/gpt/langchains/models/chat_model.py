from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler

class ChatModel:
    def __init__(
        self, temperature: float = 0, max_tokens: int = 100, is_streaming: bool = True, callbacks: list[BaseCallbackHandler] = None
    ) -> None:
        if not max_tokens > 0:
            raise ValueError("トークン数を0 < n <= 500の範囲内で指定してください")

        self._temperature = temperature
        self._max_tokens = max_tokens
        self._is_streaming = is_streaming
        self._callbacks = callbacks

        if not self._is_streaming:
            if not self._callbacks or not len(self._callbacks) > 0:
                raise ValueError('callback is empty function')

    def create_chat(self) -> ChatOpenAI:
        if not self.is_streaming:
            return ChatOpenAI(temperature=self.temperature, max_tokens=self.max_tokens)

        else:
            return ChatOpenAI(
                temperature=self._temperature,
                max_tokens=self._max_tokens,
                callbacks=self._callbacks,
                streaming=True,
            )

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, temperature: float):
        self._temperature = temperature

    @property
    def max_tokens(self):
        return self._max_tokens

    @max_tokens.setter
    def max_tokens(self, max_tokens: float):
        self._max_tokens = max_tokens

    @property
    def is_streaming(self):
        return self._is_streaming

    @is_streaming.setter
    def is_streaming(self, is_streaming: float):
        self._is_streaming = is_streaming
