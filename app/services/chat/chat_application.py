from app.apis.openai.gpt.conversion_bot import LangChainConversationChatApplication, ConversationChatBot
from abc import ABCMeta, abstractclassmethod

class ChatApplication(metaclass=ABCMeta):
    debug: bool = False

    @abstractclassmethod
    def run(self) -> str:
        pass

    @abstractclassmethod
    def conversation(self) -> None:
        pass


class ChatCommandLineApplication(ChatApplication):
    open_ai_api_app: ConversationChatBot

    def __init__(self, debug: bool) -> None:
        super().__init__()
        self.open_ai_api_app = LangChainConversationChatApplication(is_verbose=debug)
        self.debug = debug

    def run(self, prompt: str='') -> str:
        return self.open_ai_api_app.run(prompt=prompt)

    def conversation(self) -> None:
        question = input('user >> ')

        while True:
            response = self.run(prompt=question)
            print(response)
            question = input('user >> ')
            if question == 'exit':
                break


