from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import openai
import os

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

ex_template = """
これは素晴らしい! // ポジティブ
この番組は普通だった。// ニュートラル
これは酷い! // ネガティブ
あの映画は最高だった! // ポジティブ
休暇はまずまずでした。 // ニュートラル
{sentence} //
"""


class GPT3Models:
    def __init__(self, model) -> None:
        self._model = model

    @property
    def model(self):
        return self._model


class GPT3Completion(GPT3Models):
    def __init__(self, model, prompt, max_tokens=9, temperature=0) -> None:
        super().__init__(model)
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature

    def create_completion(self):
        completion = openai.Completion.create(
            model=self.model,
            prompt=self.prompt,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )

        return completion

    def create_completion_with_response_text(self) -> str:
        completion = self.create_completion()
        return completion.choices[0].text.replace('\n', '')

    @classmethod
    def input_prompt_factory(cls):
        input_prompt = cls.input_prompt()

        completion = GPT3Completion(
            model="text-davinci-003",
            prompt=input_prompt,
            max_tokens=20
        )
        completion.create_completion_with_response_text()

    def input_prompt() -> str:
        output = ""

        while True:
            input_prompt = input(" >> ")

            if input_prompt == "end":
                break

            output += input_prompt + "\n"

        return output


class BaseLLMModel:
    def __init__(self, model, temperature=None) -> None:
        self.model = model
        self.temperature = temperature
        if not temperature:
            self.temperature = 0

        self.llm = OpenAI(model_name=model, temperature=temperature)


prompt_temp = PromptTemplate(
    input_variables=["sentence"], template=ex_template)

ex_prompt = GPT3Completion.input_prompt()

completion = GPT3Completion(
    model="text-davinci-003",
    prompt=prompt_temp.format(sentence=ex_prompt),
    max_tokens=8
)
res_text = completion.create_completion_with_response_text()
print(res_text)