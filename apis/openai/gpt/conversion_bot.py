from typing import Any
from .llm_gpt import GPT3ChatCompletion
from .templates.chat_template import ChatTemplate
from .langchains.llm_chains import SearchQuestionAndAnswer
import os

class ConversationBotLangFlow:
    def __init__(self, prompt: str = '', is_verbose: bool = False) -> None:
        self.prompt = prompt
        self.is_verbose = is_verbose
        self.conversation = SearchQuestionAndAnswer(
            question_prompt=self.prompt,
            is_verbose=self.is_verbose
        )

    def __call__(self, prompt: str = '', is_verbose: bool = False) -> str:
        conversation = SearchQuestionAndAnswer(is_verbose)
        response = conversation.run(prompt=prompt)
        return response

    def run(self):
        response = self.conversation.run()
        return response

class ConversionBotDefault:
    DEFAULT_USE_MODEL = 'gpt-3.5-turbo'
    DEFAULT_MAX_TOKEN = 200
    DEFAULT_TEMPERATURE = .2
    DEFAULT_TOP_P = 0
    DEFAULT_CSV_PATH = os.getenv('CHAT_TEMPLATE_PATH')

    def __init__(self) -> None:
        self.use_model = self.DEFAULT_USE_MODEL
        self.max_token = self.DEFAULT_MAX_TOKEN
        self.temperature = self.DEFAULT_TEMPERATURE
        self.top_p = self.DEFAULT_TOP_P
        self.template_csv = self.DEFAULT_CSV_PATH
        self.templates = self._get_templates()

    def __call__(self, prompt) -> str:
        chat_completion = GPT3ChatCompletion(
            model=self.use_model,
            max_tokens=self.max_token,
            temperature=self.temperature,
            top_p=self.top_p
        )

        self.templates.append({"role": "user", "content": prompt})
        return chat_completion.create_completion(messages=self.templates)

    def _get_templates(self) -> list[dict[str, str]]:
        chat_template = ChatTemplate(self.template_csv)
        return chat_template.templates

