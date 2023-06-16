from apis.openai.gpt.langchains.llm_chains import ConversationChainChat

class TestConversationChainChat:
    chat = ConversationChainChat(is_verbose=True)

    def test_conversation_chain_chat(self):
        input_prompt = input('user（Test） >> ')

        while True:
            response = self.chat.run(input_prompt)
            print(response)
            input_prompt = input('user（Test） >> ')

            if input_prompt == 'exit':
                break


