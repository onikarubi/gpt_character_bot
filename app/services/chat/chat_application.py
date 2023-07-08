from app.apis.openai.gpt.conversion_bot import ConversationChatBot, ConversationChat
from abc import ABCMeta, abstractclassmethod

from app.apis.openai.gpt.langchains.llm_chains import ConversationChainChat

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
        self.open_ai_api_app = ConversationChatBot()
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


