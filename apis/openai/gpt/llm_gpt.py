from dotenv import load_dotenv
import openai
import os

class GPT3Model:
    def __init__(self, model) -> None:
        self.use_model = model
        self._model_list = ["gpt-3.5-turbo-0301", "gpt-3.5-turbo"]

        if not self.use_model in self._model_list:
            raise ValueError('GPT3に対応しているモデルがありません')


class GPT3Chat:
    def __init__(self, model: str = '', prompt: str = '', max_tokens=9, temperature=0) -> None:
        self.model = GPT3Model(model=model)
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature

    def create_question(self):
        content = """
            魔理沙:やや強気で物知りな女性。文法上違和感のない限りかならず「だぜ」を語尾につけてしゃべる。小学校2年生でも理解できるように説明してくれる。
            """

        completion = openai.ChatCompletion.create(
            model=self.model.use_model,
            messages=[
                {"role": "system", "content": f"あなたは次のような人物になりきって回答をしてください\n\n{content}"},
                {"role": "user", "content": "ねぇ魔理沙、最近よくChatGPTって聞くけど、何だろう？"},
                {"role": "assistant", "content": "あぁ、ChatGPTか。それはAI（人工知能）の一種で、すごく賢いコンピューターだぜ。"},
                {"role": "user", "content": self.prompt}
            ]
        )

        return completion

    def create_question_with_response_content(self) -> str:
        completion = self.create_question()
        return completion.choices[0].message.content.replace('\n', '')


class GPT3ChatFactory:
    @classmethod
    def input_prompt_factory(cls, modelname: str = "gpt-3.5-turbo"):
        cls._factory_init()
        input_prompt = cls._input_prompt()

        completion = GPT3Chat(
            model=modelname,
            prompt=input_prompt,
            max_tokens=20
        )
        result = completion.create_question_with_response_content()
        print(result)

    def _input_prompt() -> str:
        output = ""

        while True:
            input_prompt = input(" >> ")

            if input_prompt == "end":
                break

            output += input_prompt + "\n"

        return output

    def _factory_init():
        load_dotenv()
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        openai.api_key = OPENAI_API_KEY

if __name__ == "__main__":
    GPT3ChatFactory.input_prompt_factory()
