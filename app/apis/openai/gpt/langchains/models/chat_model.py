from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class ChatModel:
    def __init__(
        self, temperature: float = 0, max_tokens: int = 100, is_streaming: bool = False
    ) -> None:
        if not max_tokens > 0:
            raise ValueError("トークン数を0 < n <= 500の範囲内で指定してください")

        self._temperature = temperature
        self._max_tokens = max_tokens
        self._is_streaming = is_streaming

    def __call__(
        self, temperature: float, max_tokens: int, is_streaming: bool = False
    ) -> ChatOpenAI:
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.is_streaming = is_streaming

        return self.create_chat()

    def create_chat(self) -> ChatOpenAI:
        if not self.is_streaming:
            return ChatOpenAI(temperature=self.temperature, max_tokens=self.max_tokens)

        else:
            return ChatOpenAI(
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                callbacks=[StreamingStdOutCallbackHandler()],
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
