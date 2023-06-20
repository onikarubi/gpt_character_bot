import os
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.agents.tools import BaseTool
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
import json

class GreetingHello(BaseTool):
    name = 'greeting_hello'

    def _run():
        name = input(' >> ')
        return f'Hello {name}'



class TestChatFunction:
    @classmethod
    def setup(cls):
        cls.__OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

        cls.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613",
                         openai_api_key=cls.__OPENAI_API_KEY)

        cls.tools = [
            Tool(
                name="greeting",
                func=lambda name: f'Hello {name}!!',
                description="Return greeting"
            )
        ]

    def test_call_function(self):
        from langchain.prompts import MessagesPlaceholder
        from langchain.memory import ConversationBufferMemory

        memory = ConversationBufferMemory(
            memory_key="memory", return_messages=True)
        agent_kwargs = {
            "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
        }
        agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            agent_kwargs=agent_kwargs,
            memory=memory
        )

        agent.run(
            input={
                "content": "こんにちは",
                "function": {
                    "name": "greeting",
                    "parameters": {
                        "name": input(' >> ')
                    }
                }
            }
        )
