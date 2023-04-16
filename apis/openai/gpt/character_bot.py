from .llm_gpt import GPT3Completion
import os

FINE_TUNED_MODEL_BABBAGE = os.getenv("FINE_TUNED_MODEL_BABBAGE")

def read_prompt_template() -> str:
    with open('apis/openai/gpt/character_config_prompt.txt', "r") as f:
        r = f.read()

    return r


class CharacterBot:
    @classmethod
    def reply_character_bot_completion(cls, input_prompt: str = ''):
        prompt = read_prompt_template() + input_prompt

        gpt3_completion = GPT3Completion(
            model=FINE_TUNED_MODEL_BABBAGE,
            max_tokens=50,
            temperature=0,
            top_p=0
        )

        response = gpt3_completion.create_completion(messages=prompt)
        return response
