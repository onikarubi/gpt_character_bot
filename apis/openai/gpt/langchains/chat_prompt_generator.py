

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.chains import ConversationChain, LLMChain, SimpleSequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType, Tool
from langchain import SerpAPIWrapper
from langchain.schema import HumanMessage, SystemMessage, AIMessage, BaseMessage
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from templates.chat_template import ChatTemplate
""" データ生成用
"""

chat_templates = ChatTemplate('apis/openai/gpt/templates/chat_template.csv').templates


def generate_batch_messages() -> list[list[BaseMessage]]:
    batch_messages = []
    system_message = SystemMessage(content=chat_templates[0]['content'])

    for i in range(1, len(chat_templates), 2):
        batch_messages.append(
            system_message,
            HumanMessage(content=chat_templates[i]['content']),
            AIMessage(content=chat_templates[i + 1]['content'])
        )

    return batch_messages


def generate_chat_response(chat: ChatOpenAI, batch_messages: list[list[BaseMessage]]) -> list[str]:
    result = chat.generate(batch_messages)
    responses = []

    for generations in result.generations:
        for generation in generations:
            responses.append(generation.text)

    return responses


chat = ChatOpenAI(temperature=0)
batch_messages = generate_batch_messages()

print(batch_messages)
# responses = generate_chat_response(chat, batch_messages)
