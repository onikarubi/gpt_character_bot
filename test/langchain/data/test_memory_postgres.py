from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain.schema import messages_to_dict, messages_from_dict, AIMessage, HumanMessage
from langchain.chains import ConversationChain
from langchain.prompts.chat import AIMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain.memory import PostgresChatMessageHistory
import json
import os
import pytest


class TestChatMemoryPostgres:
    DB_USER = os.getenv('POSTGRES_USER')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    DB_HOST = os.getenv('POSTGRES_HOST')
    DB_PORT = os.getenv('POSTGRES_PORT')

    history = PostgresChatMessageHistory(
        connection_string=f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}',
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

