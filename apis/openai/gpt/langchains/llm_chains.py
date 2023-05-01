from langchain.agents import AgentType, initialize_agent, load_tools, AgentExecutor
from langchain import OpenAI
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate
from asyncio import Task
import asyncio
import datetime

class SearchQuestionAndAnswer:
    """
    質問に対する回答を検索し、指定された言語に翻訳するクラス。
    """

    def __init__(self, question: str, output_language: str, is_verbose: bool = False, max_token: int = 200) -> None:
        """
        コンストラクタ。

        :param question: 検索する質問。
        :param output_language: 出力結果の言語。
        :param is_verbose: デバッグ情報を出力するかどうか。
        """
        if max_token > 0:
            raise ValueError('トークン数を0 < n <= 500の範囲内で指定してください')

        self.llm = OpenAI(temperature=0, max_tokens=max_token)
        self.question = question
        self.output_language = output_language
        self.search_result_template = self._create_search_result_template()
        self.search_result_chain = LLMChain(
            llm=self.llm, prompt=self.search_result_template)
        self.tools = load_tools(["serpapi"])
        self.agent_chain = self._agent_init(
            agent_name=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION)
        self.overall_chain = self._create_overall_chain(verbose=is_verbose)


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
        """
        検索結果の翻訳用テンプレートを生成します。

        :return: 生成された PromptTemplate オブジェクト。
        """
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

    def _create_overall_chain(self, verbose: bool) -> SimpleSequentialChain:
        """
        エージェントチェーンと検索結果を翻訳したチェーンを組み合わせたチェーンを生成します。

        :param verbose: デバッグ情報を出力するかどうか。
        :return: 生成された SimpleSequentialChain オブジェクト。
        """
        return SimpleSequentialChain(
            chains=[self.agent_chain, self.search_result_chain],
            verbose=verbose
        )


if __name__ == '__main__':
    q_and_a = SearchQuestionAndAnswer(
        question='2022年日本の総理大臣は誰ですか？',
        output_language='日本語',
        is_verbose=False
    )

    q_and_a.run()
