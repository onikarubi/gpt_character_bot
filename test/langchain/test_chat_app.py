from app.apis.openai.gpt.langchains.llm_chains import ConversationChainChat
import pytest

is_chat_test = False

class TestConversationChainChat:
    chat = ConversationChainChat(is_verbose=True)

    @pytest.mark.skipif(is_chat_test == False, reason='Only when testing chat')
    def test_conversation_chain_chat(self):
        input_prompt = input('user（Test） >> ')

        while True:
            response = self.chat.run(input_prompt)
            print(response)
            input_prompt = input('user（Test） >> ')

            if input_prompt == 'exit':
                break


