from .langchains.llm_chains import ConversationAgentChat, ConversationChat, ConversationChainChat
from abc import ABCMeta, abstractclassmethod
import os

class ConversationChatApplication(metaclass=ABCMeta):
    conversation_app: ConversationChat

    @abstractclassmethod
    def run(self, prompt: str='') -> str:
        pass


class ConversationChatCLI(ConversationChatApplication):
    def __init__(self, prompt: str = '', is_verbose: bool = False) -> None:
        self.prompt = prompt
        self.is_verbose = is_verbose
        self.conversation_app = ConversationChainChat(
            is_streaming=True,
            display_streaming='cli'
        )

    def __call__(self, prompt: str = '') -> str:
        response = self.conversation_app.execute_chain(prompt=prompt)
        return response

    def run(self, prompt: str = ''):
        response = self.conversation_app.execute_chain(prompt)
        return response


class ConversationChatGUI(ConversationChatApplication):
    def __init__(self, container) -> None:
        self.container = container
        self.conversation_app = ConversationChainChat(
            is_streaming=True,
            display_streaming='gui',
            display_container=container
        )

    def run(self, prompt: str = ''):
        response = self.conversation_app.execute_chain(prompt)
        return response
