from langchain.agents import AgentType, initialize_agent, load_tools, AgentExecutor
from langchain import OpenAI
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate
import time

class SearchQuestionAndAnswer:
    """
    質問に対する回答を検索し、指定された言語に翻訳するクラス。
    """

    def __init__(self, question: str, output_language: str, is_verbose: bool = False) -> None:
        """
        コンストラクタ。

        :param question: 検索する質問。
        :param output_language: 出力結果の言語。
        :param is_verbose: デバッグ情報を出力するかどうか。
        """
        self.llm = OpenAI(temperature=0)
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
        質問に対する回答を検索し、指定された言語に翻訳します。
        """
        try:
            current_sec = int(time.time() % 60)
            if current_sec % 2 == 0:
                print('\rIn the middle of thinking', '/', end='', flush=True)

            else:
                print('\rIn the middle of thinking', '\\', end='', flush=True)

            response = self.overall_chain.run(self.question)
            print(response)

        except:
            print('処理を中断')
            raise

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
        エージェントチェーンと検索結果チェーンを組み合わせたチェーンを生成します。

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
