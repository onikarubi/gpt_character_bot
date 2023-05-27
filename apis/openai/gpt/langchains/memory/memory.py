from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain.schema import messages_to_dict, messages_from_dict
from langchain.chains import ConversationChain
from langchain.prompts.chat import AIMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain.chat_models import ChatOpenAI

history = ChatMessageHistory()
system_prompt = '質問に対して小学生でもわかるように優しく回答してください'
memory = ConversationBufferMemory(human_prefix='User', ai_prefix='ai', return_messages=True, memory_key='chat_history')

system_message_template = SystemMessagePromptTemplate.from_template(system_prompt)
memory.chat_memory

prompt_sample = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt),
    MessagesPlaceholder(variable_name='chat_history'),
    HumanMessagePromptTemplate.from_template('{input}'),
])

chat = ChatOpenAI()
# print(prompt_sample.input_variables)

conversation = ConversationChain(llm=chat, memory=memory, prompt=prompt_sample, verbose=True)

sample = input(' >> ')

while True:
    result = conversation.predict(input=sample)
    print(result)
    sample = input(' >> ')

    if sample == 'exit':
        break


# messages = [SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], output_parser=None, partial_variables={}, template='質問に対して小学生でもわかるように優しく回答してください', template_format='f-string', validate_template=True), additional_kwargs={}), HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], output_parser=None, partial_variables={}, template='{input}', template_format='f-string', validate_template=True), additional_kwargs={}), MessagesPlaceholder(variable_name='chat_history')]
