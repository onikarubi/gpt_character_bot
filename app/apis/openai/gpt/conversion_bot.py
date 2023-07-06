from .langchains.llm_chains import ConversationAgentChat, ConversationChat
from abc import ABCMeta, abstractclassmethod
import os

class ConversationChatApplication(metaclass=ABCMeta):
    conversation_app: ConversationChat

    @abstractclassmethod
    def run(self, prompt: str='') -> str:
        pass


class ConversationChatBot(ConversationChatApplication):
    def __init__(self, prompt: str = '', is_verbose: bool = False) -> None:
        self.prompt = prompt
        self.is_verbose = is_verbose

    def __call__(self, prompt: str = '') -> str:
        response = self.conversation_app.run(prompt=prompt)
        return response

    def run(self, prompt: str=''):
        response = self.conversation_app.run(prompt)
        return response


class LangChainConversationChatApplication(ConversationChatBot):
    def __init__(self, prompt: str = '', is_verbose: bool = False) -> None:
        super().__init__(prompt, is_verbose)
        self.conversation_app = ConversationAgentChat(
            question_prompt=self.prompt
            is_verbose=self.is_verbose
        )
