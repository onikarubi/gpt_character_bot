import json
import logging
import os
from enum import Enum
from typing import Optional, Type

from pydantic import BaseModel, Field

from langchain.agents import AgentType, initialize_agent
from langchain.agents.tools import BaseTool
from langchain.chat_models import ChatOpenAI
import openai

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

class WeatherUnit(str, Enum):
    celsius = 'celsius'
    fahrenheit = 'fahrenheit'


class GetCurrentWeatherCheckInput(BaseModel):
    location: str = Field(..., description='city_and_state')
    unit: WeatherUnit


class GetCurrentWeatherTool(BaseTool):
    name = 'get_current_weather'
    description = 'Specified location current weather acquisition.'

    def _run(self, location: str, unit: str = 'fahrenheit'):
        weather_info = {
            "location": location,
            "temperature": "72",
            "unit": unit,
            "forecast": ["sunny", "windy"],
        }
        return json.dumps(weather_info)

    def _arun(self, location: str, unit: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = GetCurrentWeatherCheckInput


class TestChatFunction:
    def setup(self):
        openai_api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = openai_api_key

        self.model = ChatOpenAI(model='gpt-3.5-turbo-0613', temperature=0)
        self.tools = [GetCurrentWeatherTool()]
        self.agent = initialize_agent(tools=self.tools, llm=self.model, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

    def test_get_current_weather_function(self, request='こんにちは、元気ですか？'):
        response = self.agent.run(request)
        logging.debug(response)



    # def test_get_current_weather_function(self):
    #     def get_current_weather(location, unit="fahrenheit"):
    #         weather_info = {
    #             "location": location,
    #             "temperature": "7",
    #             "unit": unit,
    #             "forecast": ["sunny", "windy"],
    #         }
    #         return json.dumps(weather_info)

    #     def run_conversation():
    #         # STEP1: モデルにユーザー入力と関数の情報を送る
    #         response = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo-0613",
    #             messages=[{"role": "user", "content": "ボストンの天気はどうなんだろう？"}],
    #             functions=[
    #                 {
    #                     "name": "get_current_weather",
    #                     "description": "指定した場所の現在の天気を取得",
    #                     "parameters": {
    #                         "type": "object",
    #                         "properties": {
    #                             "location": {
    #                                 "type": "string",
    #                                 "description": "都市と州（例：San Francisco, CA)",
    #                             },
    #                             "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
    #                         },
    #                         "required": ["location"],
    #                     },
    #                 }
    #             ],
    #             function_call="auto",
    #         )
    #         message = response["choices"][0]["message"]
    #         print("message>>>\n", message, "\n\n")

    #         if message.get('function_call'):
    #             function_name = message['function_call']['name']
    #             function_response = get_current_weather(
    #                 location=message.get('location'),
    #                 unit=message.get('unit')
    #             )

    #             second_message = openai.ChatCompletion.create(
    #                 model='gpt-3.5-turbo-0613',
    #                 messages=[
    #                     {"role": "user", "content": "ボストンの天気はどうなんだろう？"},
    #                     {'role': 'function', "name": function_name, 'content': function_response}
    #                 ]
    #             )

    #         return second_message

    #     print("response>>>\n", run_conversation()[
    #           "choices"][0]["message"]["content"], "\n\n")
