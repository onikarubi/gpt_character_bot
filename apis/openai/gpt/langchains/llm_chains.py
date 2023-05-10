from langchain.agents import AgentType, initialize_agent, load_tools, AgentExecutor, Tool
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, ConversationChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    AIMessagePromptTemplate,
    BaseStringMessagePromptTemplate
)
from langchain.prompts import PromptTemplate
from langchain.utilities import SerpAPIWrapper, GoogleSearchAPIWrapper
from langchain.memory import ConversationBufferMemory
from templates.chat_template import ChatTemplate
from asyncio import Task
import asyncio
import datetime
import os

class ChatModel:
    def __init__(self, temperature: float = 0, max_tokens: int = 0) -> None:
        if not max_tokens > 0:
            raise ValueError('トークン数を0 < n <= 500の範囲内で指定してください')

        self.temperature = temperature
        self.max_tokens = max_tokens

    def create_chat(self) -> ChatOpenAI:
        return ChatOpenAI(
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )


class ConversationMemory:
    def __init__(self, memory_key: str, return_messages: bool = True) -> None:
        self.memory_key = memory_key
        self.return_messages = return_messages

    def buffer_memory(self) -> ConversationBufferMemory:
        return ConversationBufferMemory(
            return_messages=self.return_messages,
            memory_key=self.memory_key
        )

class ChatPromptTemplateChain:
    CHAT_TEMPLATES: dict[str, str]

    def __init__(self) -> None:
        self.CHAT_TEMPLATES = ChatTemplate(
            os.getenv('CHAT_TEMPLATE_PATH')).templates
        self._messages_template = self._generate_messages_template()

    def _generate_messages_template(self) -> list[BaseStringMessagePromptTemplate]:
        messages_template = []

        system_message_prompt = self.get_chat_template(SystemMessagePromptTemplate, index=0)
        messages_template.append(system_message_prompt)

        for i in range(1, len(self.CHAT_TEMPLATES), 2):
            human_message_prompt = self.get_chat_template(HumanMessagePromptTemplate, index=i)
            ai_message_prompt = self.get_chat_template(AIMessagePromptTemplate, index=i + 1)
            messages_template.append(human_message_prompt)
            messages_template.append(ai_message_prompt)

        return messages_template

    def add_messages_template(self, msg_pmt_temp: BaseStringMessagePromptTemplate, prompt: str) -> None:
        self.messages_template.append(msg_pmt_temp.from_template(prompt))

    @property
    def messages_template(self):
        if not len(self._messages_template) > 0:
            return

        return self._messages_template


    def get_chat_template(self, msg_prt_temp: BaseStringMessagePromptTemplate, index: int):
        return msg_prt_temp.from_template(self.CHAT_TEMPLATES[index]['content'])

class ConversationAgents:
    SEARCH: SerpAPIWrapper | GoogleSearchAPIWrapper
    AGENT: AgentType

    def __init__(self, chat: ChatModel, verbose: bool = True) -> None:
        self.chat = chat
        self.verbose = verbose
        self.SEARCH = SerpAPIWrapper()
        self.tools = [
            Tool(
                name='Current search',
                func=self.SEARCH.run,
                description='useful for when you need to answer questions about current events or the current state of the world'
            )
        ]
        self.memory = ConversationMemory(memory_key='chat_history').buffer_memory()
        self.AGENT = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION
        self._agent_chain = self._agent_init()

    @property
    def agent_chain(self):
        return self._agent_chain

    def _agent_init(self):
        return initialize_agent(
            tools=self.tools,
            llm=self.chat,
            agent=self.AGENT_TYPE,
            memory=self.memory,
            verbose=self.verbose
        )


class SearchQuestionAndAnswer:
    """
    質問に対する回答を検索し、指定された言語に翻訳するクラス。
    """

    def __init__(self, input_prompt: str = '', is_waiting_display=False, max_tokens: int = 300, is_verbose: bool = True) -> None:
        self._input_prompt = input_prompt
        self._is_waiting_display = is_waiting_display
        self._max_tokens = max_tokens
        self._is_verbose = is_verbose
        self.chat_model = ChatModel(max_tokens=self.max_tokens)
        self.agent_chain = ConversationAgents(self.chat_model, self.is_verbose)

        self.search_result_template = self._create_search_result_template()
        self.search_result_chain = LLMChain(llm=self.llm, prompt=self.search_result_template)
        self.search = SerpAPIWrapper()
        self.tools = [
            Tool(
                name='Current search',
                func=self.search.run
            )
        ]
        self.agent_chain = self._agent_init(agent_name=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION)

    @property
    def input_prompt(self):
        return self._input_prompt

    @property
    def is_waiting_display(self):
        return self._is_waiting_display

    @property
    def max_tokens(self):
        return self._max_tokens

    @max_tokens.setter
    def max_tokens(self, tokens: int):
        self._max_tokens = tokens

    @property
    def is_verbose(self):
        return self._is_verbose

    @is_verbose.setter
    def is_verbose(self, is_verbose: bool):
        self._is_verbose = is_verbose

    def run(self):
        """
        質問に対する回答を検索し、指定された言語に翻訳された言語を出力します。
        """
        try:
            response = asyncio.run(self._thinking_task())

        except:
            print('処理を中断')
            raise

        print(response)

    async def _thinking_task(self) -> str:
        """
        質問に対する回答を非同期に取得するタスクを実行します。

        :return: 取得した回答の文字列。
        """
        task = asyncio.create_task(self._thinking())
        await self.task_waiting(task)

        print()
        return task.result()

    async def task_waiting(self, task: Task):
        """ 概要：
        タスクの完了を待つために、1秒ごとにwaiting... /またはwaiting... \を表示する。
        引数： task (Task): 完了を待つタスク。
        """
        while not task.done():
            now = datetime.datetime.now()

            if now.second % 2 == 0:
                print('\rwaiting... /', end='', flush=True)
            else:
                print('\rwaiting... \\', end='', flush=True)

            await asyncio.sleep(1)

    async def _thinking(self):
        """
        質問に対する回答を取得します。

        :return: 取得した回答の文字列。
        """
        response = await self.overall_chain.arun(self.question)
        return response

    def _create_search_result_template(self) -> PromptTemplate:
        return PromptTemplate(
            input_variables=['search_result'],
            template='{search_result}を' + self.output_language + "で翻訳してください"
        )

    def _agent_init(self, agent_name: str) -> AgentExecutor:
        """
        指定されたエージェント名でエージェントを初期化します。

        :param agent_name: 初期化するエージェント名。
        :return: 初期化された AgentExecutor オブジェクト。
        """
        return initialize_agent(
            self.tools,
            self.llm,
            agent=agent_name
        )


if __name__ == '__main__':
    q_and_a = SearchQuestionAndAnswer(
        question='2022年日本の総理大臣は誰ですか？',
        output_language='日本語',
        is_verbose=False
    )

    q_and_a.run()
