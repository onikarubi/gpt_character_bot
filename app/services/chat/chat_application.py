from apis.openai.gpt.langchains.llm_chains import SearchQuestionAndAnswer
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
    def __init__(self, debug: bool) -> None:
        super().__init__()
        self.debug = debug

    def run(self, prompt: str='') -> str:
        app = SearchQuestionAndAnswer(is_verbose=self.debug)
        return app.run(prompt)

    def conversation(self) -> None:
        question = input('user >> ')

        while True:
            response = self.run(prompt=question)
            print(response)
            question = input('user >> ')
            if question == 'exit':
                break


