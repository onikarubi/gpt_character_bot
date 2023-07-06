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
import pytest

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

    def test_get_current_weather_function(self, request='東京の天気について教えてくれますか？'):
        response = self.agent.run(request)
        logging.debug(response)

    @pytest.mark.skip(reason='confirm test exit')
    def test_call_greeting(self, request='こんにちは、元気ですか？'):
        response = self.agent.run(request)
        logging.debug(response)

