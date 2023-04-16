from apis.openai.gpt.llm_gpt import GPT3ChatCompletion

if __name__ == '__main__':
    chat = GPT3ChatCompletion(
        model='gpt-3.5-turbo'
    )
    print(chat.templates)
