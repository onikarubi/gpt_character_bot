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

chat_templates = ChatTemplate('apis/openai/gpt/templates/chat_template.csv').templates
system_message_prompt = SystemMessagePromptTemplate.from_template(chat_templates[0]['content'])

messages_template = [system_message_prompt]

for i in range(1, len(chat_templates), 2):
    messages_template.append(
        HumanMessagePromptTemplate.from_template(chat_templates[i]['content']))
    messages_template.append(
        AIMessagePromptTemplate.from_template(chat_templates[i + 1]['content']))


chat = ChatOpenAI(temperature=0)
chat_prompt_template = ChatPromptTemplate.from_messages(messages_template)
chat_prompt = chat_prompt_template.format_prompt()
messages = chat_prompt.to_messages()

for message in messages:
    print(message)

# search = SerpAPIWrapper()
# tools = [
#     Tool(
#         name='Current search',
#         func=search.run,
#         description='useful for when you need to answer questions about current events or the current state of the world'
#     )
# ]
# memory = ConversationBufferMemory(return_messages=True, memory_key='chat_history')
# agent_chain = initialize_agent(
#     tools=tools,
#     llm=chat,
#     agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
#     memory=memory,
#     verbose=True
# )

# system_msg = ''
# for templete in chat_templates:

#     if templete['role'] == 'system':
#         system_msg += templete['content'] + '\n\n'
#         continue

#     if templete['role'] == 'user':
#         role = 'ユーザー'

#     elif templete['role'] == 'assistant':
#         role = 'アシスタント'

#     else:
#         raise ValueError

#     result = f'{role}: {templete["content"]}'
#     system_msg += f'{result}\n'

# question_prompt = '現在日本の総理大臣は誰？'
# assistant_output = agent_chain.run(question_prompt)
# human_message_template = """

# 「{assistant_prompt}」を日本語に翻訳して上記の会話につづけてください。
# ユーザー：{question_prompt}
# """

# system_message_prompt = SystemMessagePromptTemplate.from_template(system_msg)
# human_message_prompt = HumanMessagePromptTemplate.from_template(human_message_template)
# messages = [system_message_prompt, human_message_prompt]

# chat_prompt_template = ChatPromptTemplate.from_messages(messages)
# chat_prompt = chat_prompt_template.format_prompt(assistant_prompt=assistant_output, question_prompt=question_prompt).to_messages()
# completion = chat(messages=chat_prompt)

# print(completion.content)

