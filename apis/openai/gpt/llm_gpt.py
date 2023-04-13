from dotenv import load_dotenv
import logs.request_logger as log
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
        try:
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

        except Exception:
            log.logger_output(level='error', message=f'chatgpt apiの処理中に問題が発生しました')
            raise

    def create_question_with_response_content(self) -> str:
        completion = self.create_question()
        return completion.choices[0].message.content.replace('\n', '')


class GPT3ChatFactory:
    @classmethod
    def output_prompt(cls,input_prompt: str, modelname: str = "gpt-3.5-turbo") -> str:
        cls._factory_init()
        completion = GPT3Chat(
            model=modelname,
            prompt=input_prompt,
            max_tokens=20
        )
        return completion.create_question_with_response_content()

    def _factory_init() -> None:
        load_dotenv()
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        openai.api_key = OPENAI_API_KEY


if __name__ == "__main__":
    pass
