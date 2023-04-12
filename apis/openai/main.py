from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from chat_api.chatgpt import GPT3Completion
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


def input_prompt() -> str:
    output = ""

    while True:
        input_prompt = input(" >> ")

        if input_prompt == "end":
            break

        output += input_prompt + "\n"

    return output


prompt_temp = PromptTemplate(
    input_variables=["sentence"], template=ex_template)

ex_prompt = input_prompt()

completion = GPT3Completion(
    model="text-davinci-003",
    prompt=prompt_temp.format(sentence=ex_prompt),
    max_tokens=8
)
res_text = completion.create_completion_with_response_text()
print(res_text)





# llm = OpenAI(temperature=.5)

# print(llm('カラフルな靴下を作る会社の社名として、何かいいものはないですか？日本語の社名でお願いします。'))
