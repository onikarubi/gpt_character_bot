from langchain.memory import ConversationBufferMemory
import abc
import dataclasses


@dataclasses.dataclass
class ChatMemory(metaclass=abc.ABCMeta):
    memory_key: str
    return_messages: bool


class ConversationMemory:
    def __init__(self, memory_key: str, return_messages: bool = True) -> None:
        self.memory_key = memory_key
        self.return_messages = return_messages

    def buffer_memory(self) -> ConversationBufferMemory:
        return ConversationBufferMemory(
            return_messages=self.return_messages, memory_key=self.memory_key
        )
