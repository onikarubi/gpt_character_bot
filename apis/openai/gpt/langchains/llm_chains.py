from gc import callbacks
from types import coroutine
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
    BaseStringMessagePromptTemplate,
    BaseMessagePromptTemplate
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.utilities import SerpAPIWrapper, GoogleSearchAPIWrapper, GoogleSerperAPIWrapper
from langchain.memory import ConversationBufferMemory
from ..templates.chat_template import ChatTemplate
from asyncio import Task
import asyncio
import datetime
import os

class ChatModel:
    def __init__(self, temperature: float = 0, max_tokens: int = 0, is_streaming: bool = False) -> None:
        if not max_tokens > 0:
            raise ValueError('トークン数を0 < n <= 500の範囲内で指定してください')

        self.temperature = temperature
        self.max_tokens = max_tokens
        self.is_streaming = is_streaming

    def create_chat(self) -> ChatOpenAI:
        if not self.is_streaming:
            return ChatOpenAI(
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

        else:
            return ChatOpenAI(
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                callbacks=[StreamingStdOutCallbackHandler()],
                streaming=True
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

class ChatPromptTemplateGenerator:
    CHAT_TEMPLATES: dict[str, str]

    def __init__(self) -> None:
        self.CHAT_TEMPLATES = ChatTemplate(
            os.getenv('CHAT_TEMPLATE_PATH')).templates
        self._messages_template = self._generate_conversation_templates()

    def _generate_conversation_templates(self) -> list[BaseStringMessagePromptTemplate]:
        messages_template = []

        system_message_prompt = self._get_chat_template(SystemMessagePromptTemplate, index=0)
        messages_template.append(system_message_prompt)

        for i in range(1, len(self.CHAT_TEMPLATES), 2):
            human_message_prompt = self._get_chat_template(HumanMessagePromptTemplate, index=i)
            ai_message_prompt = self._get_chat_template(AIMessagePromptTemplate, index=i + 1)
            messages_template.append(human_message_prompt)
            messages_template.append(ai_message_prompt)

        return messages_template

    def add_messages_template(self, msg_pmt_temp: BaseStringMessagePromptTemplate, prompt: str) -> None:
        self.messages_template.append(msg_pmt_temp.from_template(prompt))

    def _get_chat_template(self, msg_prt_temp: BaseStringMessagePromptTemplate, index: int) -> BaseMessagePromptTemplate:
        return msg_prt_temp.from_template(self.CHAT_TEMPLATES[index]['content'])

    def get_chat_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(self.messages_template)

    @property
    def messages_template(self) -> list[BaseStringMessagePromptTemplate]:
        if not len(self._messages_template) > 0:
            return

        return self._messages_template


class ConversationAgents:
    SEARCH: SerpAPIWrapper | GoogleSearchAPIWrapper | GoogleSerperAPIWrapper
    AGENT_TYPE: AgentType

    def __init__(self, chat: ChatOpenAI, verbose: bool = True) -> None:
        self.chat = chat
        self.verbose = verbose
        self.SEARCH = GoogleSerperAPIWrapper()
        self._tools = [
            Tool(
                name='Current search',
                func=self.SEARCH.run,
                description='useful for when you need to answer questions about current events or the current state of the world',
                coroutine=self.SEARCH.arun
            )
        ]
        self.memory = ConversationMemory(memory_key='chat_history').buffer_memory()
        self.AGENT_TYPE = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION

    def agent_chain(self):
        return self._agent_init()

    @property
    def tools(self):
        if not len(self._tools) > 0:
            return

        return self._tools

    def add_tool(self, tool: Tool):
        self.tools.append(tool)

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
    CHAT_MODEL: ChatModel
    AGENTS: ConversationAgents
    DEFAULT_QUESTION_PROMPT = '現在日本の総理大臣は誰？'
    DEFAULT_ANSWERED_PROMPT = """
    {input_question}という質問に対して、
    {input_answer}を日本語に直して上記の会話のように回答して。
    """

    def __init__(self, question_prompt: str = DEFAULT_QUESTION_PROMPT, is_streaming=False, max_tokens: int = 300) -> None:
        self._question_prompt = question_prompt
        self._answered_prompt = self.DEFAULT_ANSWERED_PROMPT
        self._is_streaming = is_streaming
        self._max_tokens = max_tokens
        
        if self._is_streaming:
            self.is_verbose = False
        else:
            self.is_verbose = True

        self.CHAT_MODEL = ChatModel(max_tokens=self.max_tokens, is_streaming=self.is_streaming)
        self.llm_chat = self.CHAT_MODEL.create_chat()
        self.AGENTS = ConversationAgents(self.llm_chat, self.is_verbose)
        self.agent_chain = self.AGENTS.agent_chain()
        self.chat_prompt_generator = ChatPromptTemplateGenerator()


    @property
    def question_prompt(self):
        return self._question_prompt

    @question_prompt.setter
    def question_prompt(self, prompt: str):
        self._question_prompt = prompt
        
    @property
    def answered_prompt(self):
        return self._answered_prompt

    @property
    def is_streaming(self):
        return self._is_streaming

    @property
    def max_tokens(self):
        return self._max_tokens

    @max_tokens.setter
    def max_tokens(self, tokens: int):
        self._max_tokens = tokens

    def run(self, prompt: str = ''):
        """
        質問に対する回答を検索し、指定された言語に翻訳された言語を出力します。
        """
        if prompt:
            self.question_prompt = prompt

        try:
            if not self.is_streaming:
                response = asyncio.run(self._athinking_task())
            else:
                response = self._thinking_task()

        except:
            print('処理を中断')
            raise

        print(response)

    def _thinking_task(self) -> str:
        """
        質問に対する回答を同期に取得するタスクを実行します。

        :return: 取得した回答の文字列。
        """
        task_agent = self._thinking_agent()
        task_result = self._thinking_template_chain(task_agent)
        return task_result

    def _thinking_agent(self) -> str:
        try:
            result_output = self.agent_chain.run(self.question_prompt)
            return result_output

        except ValueError:
            err_msg = "APIのリクエスト上限に到達しました。"
            print(self._running_exception_msg(
                place='エージェントツール', reason=err_msg))
            raise ValueError(err_msg)

        except Exception as e:
            print(self._running_exception_msg(place='エージェントツール', reason=e))
            raise

    def _thinking_template_chain(self, agent_answer: str) -> str:
        try:
            self.chat_prompt_generator.add_messages_template(
                msg_pmt_temp=HumanMessagePromptTemplate,
                prompt=self.answered_prompt
            )
            chat_prompt_template = self.chat_prompt_generator.get_chat_prompt_template()
            result_chain = LLMChain(llm=self.llm_chat,
                                    prompt=chat_prompt_template)
            response = result_chain.run(
                input_question=self.question_prompt + '上記の会話に続けて回答してください', input_answer=agent_answer)
            return response

        except:
            print('テンプレート処理にてエラーが発生')
            raise

    async def _athinking_task(self) -> str:
        """
        質問に対する回答を非同期に取得するタスクを実行します。

        :return: 取得した回答の文字列。
        """
        task = asyncio.create_task(self._athinking())
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

    async def _athinking(self) -> str:
        agent_answer = await self._athinking_agent()
        result = await self._athinking_template_chain(agent_answer)
        return result

    async def _athinking_agent(self):
        try:
            result_output = await self.agent_chain.arun(self.question_prompt)
            return result_output

        except ValueError:
            err_msg = "APIのリクエスト上限に到達しました。"
            print(self._running_exception_msg(place='エージェントツール', reason=err_msg))
            raise ValueError(err_msg)

        except Exception as e:
            print(self._running_exception_msg(place='エージェントツール', reason=e))
            raise

    async def _athinking_template_chain(self, agent_answer: str):
        try:
            self.chat_prompt_generator.add_messages_template(
                msg_pmt_temp=HumanMessagePromptTemplate,
                prompt=self.answered_prompt
            )
            chat_prompt_template = self.chat_prompt_generator.get_chat_prompt_template()
            result_chain = LLMChain(llm=self.llm_chat,
                                    prompt=chat_prompt_template)
            response = await result_chain.arun(input_question=self.question_prompt + '上記の会話に続けて回答してください', input_answer=agent_answer)
            return response

        except:
            print('テンプレート処理にてエラーが発生')
            raise

    def _running_exception_msg(self, place: str, reason: str) -> str:
        return f"{place}でエラーが発生。\n原因: \n{reason}"

if __name__ == '__main__':
    q_and_a = SearchQuestionAndAnswer(
        question_prompt='今日の日本の天気予報を教えて',
    )
    q_and_a.run()
