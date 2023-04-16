from abc import ABCMeta, abstractmethod
from dotenv import load_dotenv
from typing import Union
from logs.request_logger import logger_output
import csv
import openai
import os

load_dotenv()

class GPT3Model(metaclass=ABCMeta):
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    def __init__(
        self,
        model: str,
        supported_models: list[str] = None,
        max_tokens: int = 100,
        temperature: float = 0,
        top_p: float = 0
    ) -> None:
        self._use_model = model
        self.supported_models = supported_models
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        openai.api_key = self.OPENAI_API_KEY

    @property
    def use_model(self):
        if not self._use_model or not self._use_model in self.supported_models:
            raise ValueError('対応しているモデルはありません')

        return self._use_model

    @abstractmethod
    def create_completion(self, messages: Union[str, dict[str, any]]): pass


class GPT3Completion(GPT3Model):
    COMPLETION_SUPPORTED_MODELS = ["davinci", "curie", "text-davinci-003"]

    def __init__(self, model: str, supported_models: list[str] = None, max_tokens: int = 100, temperature: float = 0, top_p: float = 0) -> None:
        super().__init__(model, supported_models, max_tokens, temperature, top_p)
        self.supported_models = self.COMPLETION_SUPPORTED_MODELS

    def create_completion(self, messages: Union[str, dict[str, any]]):
        try:
            completion = openai.Completion.create(
                model=self.use_model,
                prompt=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p
            )

            response_content = completion.choices[0].text.replace('\n', '')
            success_msg = f"""
            メッセージの生成が完了しました。
            内容:

            {response_content}
            """
            logger_output(level='info', message=success_msg, output_filename='openai_access')
            return response_content

        except:
            error_msg = f"""
            {self.create_completion}でエラーが発生しました。設定を見直して下さい
            response >> {response_content}
            """
            logger_output(level='error', message=error_msg)
            raise


class GPT3ChatCompletion(GPT3Model):
    CHAT_COMPLETION_SUPPORTED_MODELS = ['gpt-3.5-turbo', "gpt-3.5-turbo-0301"]

    def __init__(self, model: str, supported_models: list[str] = None, max_tokens: int = 100, temperature: float = 0, top_p: float = 0) -> None:
        super().__init__(model, supported_models, max_tokens, temperature, top_p)
        self.supported_models = self.CHAT_COMPLETION_SUPPORTED_MODELS
        self.templates = [i for i in self.get_templates()]

    def create_completion(self, messages: Union[str, dict[str, any]]):
        pass

    def get_templates(self) -> list[dict[str, str]]:
        with open('apis/openai/gpt/templates/chat_template.csv') as csv_file:
            templates = csv.DictReader(csv_file)

            return [template for template in templates]

# class GPT3ChatCompletion:
#     def __init__(self, model: str = '', prompt: str = '', max_tokens=9, temperature=0) -> None:
#         self.model = GPT3Model(model=model)
#         self.prompt = prompt
#         self.max_tokens = max_tokens
#         self.temperature = temperature

#     def create_completion(self):
#         content = """
#             魔理沙:やや強気で物知りな女性。文法上違和感のない限りかならず「だぜ」を語尾につけてしゃべる。小学校2年生でも理解できるように説明してくれる。
#             """
#         try:
#             completion = openai.ChatCompletion.create(
#                 model=self.model.use_model,
#                 messages=[
#                     {"role": "system",
#                         "content": f"あなたは次のような人物になりきって回答をしてください\n\n{content}"},
#                     {"role": "user", "content": "ねぇ魔理沙、最近よくChatGPTって聞くけど、何だろう？"},
#                     {"role": "assistant",
#                         "content": "あぁ、ChatGPTか。それはAI（人工知能）の一種で、すごく賢いコンピューターだぜ。"},
#                     {"role": "user", "content": self.prompt}
#                 ]
#             )
#             response_msg = self._create_question_with_response_content(
#                 completion)
#             success_msg = f"""
#             メッセージの生成が完了しました。
#             内容:

#             {response_msg}
#             """
#             logger_output(file_output='openai_access',
#                           level='info', message=success_msg)
#             return response_msg

#         except Exception:
#             logger_output(file_output='openai_access', level='error', message=f'chatgpt apiの処理中に問題が発生しました')
#             raise

#     def _create_question_with_response_content(self, msg_content: str) -> str:
#         return msg_content.choices[0].message.content.replace('\n', '')

