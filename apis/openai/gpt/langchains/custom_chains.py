from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    AIMessagePromptTemplate
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

chat = ChatOpenAI(temperature=0)

"""
チャットテンプレートの初期化
"""
chat_templates = ChatTemplate('apis/openai/gpt/templates/chat_template.csv').templates
system_message_prompt = SystemMessagePromptTemplate.from_template(chat_templates[0]['content'])

messages_template = [system_message_prompt]

for i in range(1, len(chat_templates), 2):
    messages_template.append(
        HumanMessagePromptTemplate.from_template(chat_templates[i]['content']))
    messages_template.append(
        AIMessagePromptTemplate.from_template(chat_templates[i + 1]['content']))


"""
エージェントツールを用いて質問のプロンプトに対して検索をかける
"""

search = SerpAPIWrapper()
tools = [
    Tool(
        name='Current search',
        func=search.run,
        description='useful for when you need to answer questions about current events or the current state of the world'
    )
]
memory = ConversationBufferMemory(return_messages=True, memory_key='chat_history')
agent_chain = initialize_agent(
    tools=tools,
    llm=chat,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

question_prompt = '現在日本の総理大臣は誰？'
assistant_output = agent_chain.run(question_prompt)

human_message_prompt = """
{input_question}という質問に対して、
{input_answer}を日本語に直して上記の会話のように回答して。
"""
messages_template.append(HumanMessagePromptTemplate.from_template(human_message_prompt))

chat_prompt_template = ChatPromptTemplate.from_messages(messages_template)
chain = LLMChain(llm=chat, prompt=chat_prompt_template)
completion = chain.run(input_question=question_prompt, input_answer=assistant_output)
print(completion)

