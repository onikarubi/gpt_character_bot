from langchain.agents import (
    AgentType,
    initialize_agent,
    load_tools,
    AgentExecutor,
    Tool,
)
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, ConversationChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    BaseStringMessagePromptTemplate,
    BaseMessagePromptTemplate,
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.utilities import SerpAPIWrapper, GoogleSerperAPIWrapper
from langchain.memory import ConversationBufferMemory
from ..templates.chat_template import ChatTemplate
from asyncio import Task
import asyncio
import datetime
import os


class ChatModel:
    def __init__(
        self, temperature: float = 0, max_tokens: int = 100, is_streaming: bool = False
    ) -> None:
        if not max_tokens > 0:
            raise ValueError("トークン数を0 < n <= 500の範囲内で指定してください")

        self._temperature = temperature
        self._max_tokens = max_tokens
        self._is_streaming = is_streaming

    def __call__(
        self, temperature: float, max_tokens: int, is_streaming: bool = False
    ) -> ChatOpenAI:
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.is_streaming = is_streaming

        return self.create_chat()

    def create_chat(self) -> ChatOpenAI:
        if not self.is_streaming:
            return ChatOpenAI(temperature=self.temperature, max_tokens=self.max_tokens)

        else:
            return ChatOpenAI(
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                callbacks=[StreamingStdOutCallbackHandler()],
                streaming=True,
            )

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, temperature: float):
        self._temperature = temperature

    @property
    def max_tokens(self):
        return self._max_tokens

    @max_tokens.setter
    def max_tokens(self, max_tokens: float):
        self._max_tokens = max_tokens

    @property
    def is_streaming(self):
        return self._is_streaming

    @is_streaming.setter
    def is_streaming(self, is_streaming: float):
        self._is_streaming = is_streaming


class ConversationMemory:
    def __init__(self, memory_key: str, return_messages: bool = True) -> None:
        self.memory_key = memory_key
        self.return_messages = return_messages

    def buffer_memory(self) -> ConversationBufferMemory:
        return ConversationBufferMemory(
            return_messages=self.return_messages, memory_key=self.memory_key
        )


class ChatPromptTemplateGenerator:
    CHAT_TEMPLATES: dict[str, str]

    def __init__(self) -> None:
        self.CHAT_TEMPLATES = ChatTemplate(os.getenv("CHAT_TEMPLATE_PATH")).templates
        self._messages_template = self._generate_conversation_templates()

    # 事前会話用のテンプレートを生成
    def _generate_conversation_templates(self) -> list[BaseStringMessagePromptTemplate]:
        messages_template = []

        system_message_prompt = self._get_chat_template(
            SystemMessagePromptTemplate, index=0
        )
        messages_template.append(system_message_prompt)

        for i in range(1, len(self.CHAT_TEMPLATES), 2):
            human_message_prompt = self._get_chat_template(
                HumanMessagePromptTemplate, index=i
            )
            ai_message_prompt = self._get_chat_template(
                AIMessagePromptTemplate, index=i + 1
            )
            messages_template.append(human_message_prompt)
            messages_template.append(ai_message_prompt)

        return messages_template

    def _get_chat_template(
        self, msg_prt_temp: BaseStringMessagePromptTemplate, index: int
    ) -> BaseMessagePromptTemplate:
        return msg_prt_temp.from_template(self.CHAT_TEMPLATES[index]["content"])

    def add_messages_template(
        self, msg_pmt_temp: BaseStringMessagePromptTemplate, prompt: str
    ) -> None:
        self.messages_template.append(msg_pmt_temp.from_template(prompt))

    def get_chat_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(self.messages_template)

    @property
    def messages_template(self) -> list[BaseStringMessagePromptTemplate]:
        if not len(self._messages_template) > 0:
            return

        return self._messages_template


class ConversationAgents:
    AGENT_TYPE: AgentType

    def __init__(self, chat: ChatOpenAI, verbose: bool = True) -> None:
        self.chat = chat
        self.verbose = verbose
        self.search_tools = {
            "serpapi": self._search_tool(SerpAPIWrapper),
            "google-serper": self._search_tool(GoogleSerperAPIWrapper),
        }
        self.tools = [self.get_search_tool("google-serper")]
        self.memory = ConversationMemory(memory_key="chat_history").buffer_memory()
        self.AGENT_TYPE = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION

    def _search_tool(
        self, api_wrapper: SerpAPIWrapper | GoogleSerperAPIWrapper
    ) -> tuple[Tool | SerpAPIWrapper | GoogleSerperAPIWrapper]:
        search_api_wrapper = api_wrapper()
        title = "Current search"
        description = "時事問題や最新の情報に対応してくれる"

        return (
            Tool(
                name=title,
                description=description,
                func=search_api_wrapper.run,
                coroutine=search_api_wrapper.arun,
            ),
            api_wrapper,
        )

    def get_search_tool(self, searcher: str) -> Tool:
        if searcher == "serpapi":
            return self.search_tools["serpapi"][0]

        elif searcher == "google-serper":
            return self.search_tools["google-serper"][0]

        else:
            raise ValueError

    def agent_chain(self) -> AgentExecutor:
        return initialize_agent(
            tools=self.tools,
            llm=self.chat,
            agent=self.AGENT_TYPE,
            memory=self.memory,
            verbose=self.verbose,
        )

    def change_search_tool(
        self, change_tool: Tool, label_name: str = "Current search"
    ) -> None:
        for i in range(len(self.tools)):
            if not self.tools[i].name == label_name:
                continue

            self.tools[i] = change_tool
            return

    def add_tool(self, tool: Tool):
        self.tools.append(tool)


class SearchQuestionAndAnswer:
    """
    質問に対する回答を検索し、指定された言語に翻訳するクラス。
    """

    CHAT_MODEL: ChatModel
    AGENTS: ConversationAgents

    def __init__(
        self, question_prompt: str = "", is_verbose: bool = False
    ) -> None:
        self._question_prompt = question_prompt
        self.is_verbose = is_verbose
        self.CHAT_MODEL = ChatModel()
        self.task_model = self.CHAT_MODEL(
            temperature=0, max_tokens=200, is_streaming=False
        )
        self.AGENTS = ConversationAgents(chat=self.task_model, verbose=self.is_verbose)
        self._agent_chain = self.AGENTS.agent_chain()
        self.chat_prompt_generator = ChatPromptTemplateGenerator()

    @property
    def question_prompt(self):
        return self._question_prompt

    @question_prompt.setter
    def question_prompt(self, prompt: str):
        self._question_prompt = prompt

    @property
    def agent_chain(self):
        return self._agent_chain

    def change_chat_model(self, target_name: str, new_chat_model: ChatModel) -> None:
        if target_name == "llm_chat":
            self.llm_chat = new_chat_model.create_chat()
            return

        elif target_name == "agent":
            self.task_model = new_chat_model.create_chat()
            return

        else:
            raise ValueError

    def run(self, prompt: str = "") -> str:
        """
        質問に対する回答を検索し、指定された言語に翻訳された言語を出力します。
        """
        if prompt:
            self.question_prompt = prompt

        try:
            response = self._thinking_task()

        except:
            print("処理を中断")
            raise

        print(response)
        return response

    def _thinking_task(self) -> str:
        """
        質問に対する回答を同期に取得するタスクを実行します。

        :return: 取得した回答の文字列。”
        """
        task_agent = self._thinking_agent()
        task_result = self._thinking_template_chain(task_agent)
        return task_result

    def _thinking_agent(self) -> str:
        try:
            agent_answer = f'{self.question_prompt}\n最低50文字以上で解説してください'
            result_output = self.agent_chain.run(input=agent_answer)
            return result_output

        except Exception as e:
            print(self._running_exception_msg(place="エージェントツール", reason=e))
            raise

    def _thinking_template_chain(self, agent_answer: str) -> str:
        try:
            # ユーザーからのリクエストに対するテンプレートのデータを追加
            answer_prompt = '{agent_answer}を日本語に直して会話を続けてね'
            self.chat_prompt_generator.add_messages_template(
                msg_pmt_temp=HumanMessagePromptTemplate, prompt=answer_prompt
            )

            chat_prompt_template = self.chat_prompt_generator.get_chat_prompt_template()
            result_chain = LLMChain(llm=self.task_model, prompt=chat_prompt_template)
            response = result_chain.run(agent_answer=agent_answer)
            return response

        except:
            print("テンプレート処理にてエラーが発生")
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
        """概要：
        タスクの完了を待つために、1秒ごとにwaiting... /またはwaiting... \を表示する。
        引数： task (Task): 完了を待つタスク。
        """
        while not task.done():
            now = datetime.datetime.now()

            if now.second % 2 == 0:
                print("\rwaiting... /", end="", flush=True)
            else:
                print("\rwaiting... \\", end="", flush=True)

            await asyncio.sleep(1)

    async def _athinking(self) -> str:
        agent_answer = await self._athinking_agent()
        result = await self._athinking_template_chain(agent_answer)
        return result

    async def _athinking_agent(self):
        while True:
            try:
                result_output = await self.agent_chain.arun(self.question_prompt)
                print(result_output)
                return result_output

            except ValueError:
                err_msg = "APIのリクエスト上限に到達しました。"
                print(self._running_exception_msg(place="エージェントツール", reason=err_msg))
                self.AGENTS.change_search_tool(
                    self.AGENTS.get_search_tool("google-serper")
                )

            except Exception as e:
                print(self._running_exception_msg(place="エージェントツール", reason=e))
                raise

    async def _athinking_template_chain(self, agent_answer: str):
        try:
            self.chat_prompt_generator.add_messages_template(
                msg_pmt_temp=HumanMessagePromptTemplate, prompt=self.answered_prompt
            )
            chat_prompt_template = self.chat_prompt_generator.get_chat_prompt_template()
            result_chain = LLMChain(llm=self.llm_chat, prompt=chat_prompt_template)
            response = await result_chain.arun(
                input_question=self.question_prompt, input_answer=agent_answer
            )
            return response

        except:
            print("テンプレート処理にてエラーが発生")
            raise

    def _running_exception_msg(self, place: str, reason: str) -> str:
        return f"{place}でエラーが発生。\n原因: \n{reason}"
