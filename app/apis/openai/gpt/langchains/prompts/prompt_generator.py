from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    BaseStringMessagePromptTemplate,
    BaseMessagePromptTemplate,
    MessagesPlaceholder
)
from ...templates.chat_template import ChatTemplate
import os

class ChatPromptTemplateGenerator:
    CHAT_TEMPLATES: dict[str, str]

    def __init__(self) -> None:
        self.CHAT_TEMPLATES = ChatTemplate(
            os.getenv("CHAT_TEMPLATE_PATH")).templates
        self._messages_template = self._generate_conversation_templates()

    # 事前会話用のテンプレートを生成
    def _generate_conversation_templates(self) -> list[BaseStringMessagePromptTemplate]:
        messages_template = []

        system_message_prompt = self._get_chat_template(
            SystemMessagePromptTemplate, index=0
        )
        messages_template.append(system_message_prompt)

        for i in range(1, len(self.CHAT_TEMPLATES), 2):
            human_message_prompt = self._get_chat_template(
                HumanMessagePromptTemplate, index=i
            )
            ai_message_prompt = self._get_chat_template(
                AIMessagePromptTemplate, index=i + 1
            )
            messages_template.append(human_message_prompt)
            messages_template.append(ai_message_prompt)

        return messages_template

    def _get_chat_template(
        self, msg_prt_temp: BaseStringMessagePromptTemplate, index: int
    ) -> BaseMessagePromptTemplate:
        return msg_prt_temp.from_template(self.CHAT_TEMPLATES[index]["content"])

    def add_messages_template(
        self, msg_pmt_temp: BaseStringMessagePromptTemplate, prompt: str
    ) -> None:
        self.messages_template.append(msg_pmt_temp.from_template(prompt))

    def add_messages_placeholder(self, variable_name: str) -> None:
        messages_placeholder = MessagesPlaceholder(variable_name=variable_name)
        self.messages_template.append(messages_placeholder)

    def get_chat_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(self.messages_template)

    @property
    def messages_template(self) -> list[BaseStringMessagePromptTemplate]:
        if not len(self._messages_template) > 0:
            return

        return self._messages_template
