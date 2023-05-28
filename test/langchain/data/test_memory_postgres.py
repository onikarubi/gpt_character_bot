from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain.schema import messages_to_dict, messages_from_dict, AIMessage, HumanMessage
from langchain.chains import ConversationChain
from langchain.prompts.chat import AIMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain.memory import PostgresChatMessageHistory
from apis.openai.gpt.langchains.memory.db_memory import POSTGRES_USER, POSTGRES_PORT, POSTGRES_PASSWORD, POSTGRES_HOST
import json
import os
import pytest


class TestChatMemoryPostgres:
    history = PostgresChatMessageHistory(
        connection_string=f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}',
        session_id='test-session'
    )

    def test_add_messages(self):
        self.history.add_user_message('hi')
        self.history.add_ai_message('whats up?')

    def test_assert_values(self):
        for message in self.history.messages:
            if type(message) == HumanMessage:
                assert message.content == 'hi'

            elif type(message) == AIMessage:
                assert message.content == 'whats up?'

            else:
                raise TypeError

    """ 
    テストデータを削除する
    """
    def test_clean_data(self):
        self.history.clear()

