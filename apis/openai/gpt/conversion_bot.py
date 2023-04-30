from .llm_gpt import GPT3ChatCompletion
import csv

class ConversionBot:
    DEFAULT_USE_MODEL = 'gpt-3.5-turbo'
    DEFAULT_MAX_TOKEN = 200
    DEFAULT_TEMPERATURE = .2
    DEFAULT_TOP_P = 0

    def __init__(self) -> None:
        self.use_model = self.DEFAULT_USE_MODEL
        self.max_token = self.DEFAULT_MAX_TOKEN
        self.temperature = self.DEFAULT_TEMPERATURE
        self.top_p = self.DEFAULT_TOP_P
        self.template_csv = 'apis/openai/gpt/templates/chat_template.csv'
        self.templates = self._get_templates()

    def __call__(self, prompt) -> str:
        chat_completion = GPT3ChatCompletion(
            model=self.use_model,
            max_tokens=self.max_token,
            temperature=self.temperature,
            top_p=self.top_p
        )

        self.templates.append({"role": "user", "content": prompt})
        return chat_completion.create_completion(messages=self.templates)

    def _get_templates(self) -> list[dict[str, str]]:
        with open(self.template_csv) as csv_file:
            templates = csv.DictReader(csv_file)

            return [template for template in templates]


