from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

class BaseLLMModel:
    def __init__(self, model, temperature=None) -> None:
        self.model = model
        self.temperature = temperature
        if not temperature:
            self.temperature = 0

        self.llm = OpenAI(model_name=model, temperature=temperature)


