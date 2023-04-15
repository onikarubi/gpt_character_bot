from .llm_gpt import GPT3Completion


def read_prompt_template() -> str:
    with open('apis/openai/gpt/character_config_prompt.txt', "r") as f:
        r = f.read()

    return r


class CharacterBot:
    @classmethod
    def reply_character_bot_completion(cls, input_prompt: str = ''):
        prompt = read_prompt_template() + input_prompt

        gpt3_completion = GPT3Completion(
            model='text-davinci-003',
            max_tokens=100,
            temperature=0,
            top_p=0
        )

        response = gpt3_completion.create_completion(messages=prompt)
        return response
