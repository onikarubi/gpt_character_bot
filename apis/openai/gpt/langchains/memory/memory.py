import abc
import dataclasses

@dataclasses.dataclass
class ChatMemory(metaclass=abc.ABCMeta):
    memory_key: str
    return_messages: bool

