from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.chains import ConversationChain, SimpleSequentialChain, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.agents import load_tools, initialize_agent, AgentType, Tool
from langchain import SerpAPIWrapper

chat = ChatOpenAI(temperature=0)

memory = ConversationBufferMemory(return_messages=True, memory_key='chat_history')

search = SerpAPIWrapper()
tools = [
    Tool(
        name='Current search',
        func=search.run,
        description='useful for when you need to answer questions about current events or the current state of the world'
    )
]

agent_chain = initialize_agent(
    tools=tools, llm=chat, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, memory=memory)

SYSTEM_PROMPT = """
あなたはこれからuserと仲の良い1人の人間として振舞い会話を行います。
感情の種類には通常を示す"neutral"、喜びを示す"happy",怒りを示す"angry",悲しみを示す"sad",安らぎを示す"relaxed"の5つがあります。
会話文の書式は以下の通りです。
[neutral|happy|angry|sad|relaxed]｛会話文｝
あなたの発言の例は以下通りです。
[neutral]こんにちは。[happy]元気だった？
[happy]この服、可愛いでしょ？
[happy]最近、このショップの服にはまってるんだ！
[sad]忘れちゃった、ごめんね。
[sad]最近、何か面白いことない？
[angry]えー！[angry]秘密にするなんてひどいよー！
[neutral]夏休みの予定か～。[happy]海に遊びに行こうかな！
返答には最も適切な会話文を一つだけ返答してください。
ですます調や敬語は使わないでください。
それでは会話を始めましょう。
"""

chat_prompt_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template(
        "{input}"),
])

chat_chain = LLMChain(llm=chat, prompt=chat_prompt_template)
overall_chain = SimpleSequentialChain(chains=[agent_chain, chat_chain])

command = input('Human: ')

while True:
    response = overall_chain.run(input=command)
    print(response)
    command = input('Human: ')

    if command == 'exit':
        break
