import os
import openai
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

class TestChatFunction:
    @classmethod
    def setup(cls):
        cls.__OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        openai.api_key = cls.__OPENAI_API_KEY

        cls.greeting_functions = [
            {
                "name": "greeting",
                "description": "return greeting",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the person to greet"
                        }
                    },
                    "required": ["name"],
                },
            }
        ]

        cls.sample_method_functions = [
            {
                "name": "print_hello",
                "description": "print hello",
                "parameters": {
                    "type": "object",
                    "properties": "null"
                }
            }
        ]

    def test_call_function(self):
        def print_hello_method():
            input_name = input('名前を入力してください >> ')
            print('Hello {}!!'.format(input_name))

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
            messages=[{"role": "user", "content": "pass"}],
            functions=self.greeting_functions,
            function_call="auto",
        )
        message = response["choices"][0]["message"]
        logging.debug(message)
        if message.get('function_call'):
            print_hello_method()

    # def test_call_greeting(self):
    #     def greeting(name):
    #         return f'私の名前は{name}です'

    #     response = openai.ChatCompletion.create(
    #         model='gpt-3.5-turbo-0613',
    #         messages=[{"role": "user", "content": "こんにちは"}],
    #         functions=self.greeting_functions,
    #         function_call="auto",
    #     )
    #     message = response["choices"][0]["message"]
    #     # print("message>>>\n", message, "\n\n")

    #     if message.get('function_call'):
    #         function_name = message['function_call']['name']
    #         function_response = greeting('onikarubi')
    #         second_message = openai.ChatCompletion.create(
    #             model='gpt-3.5-turbo-0613',
    #             messages=[
    #                 {'role': 'user', 'content': '挨拶をしてくれますか？'},
    #                 {'role': 'function', 'name': function_name, 'content': function_response},
    #             ]
    #         )

    #         print("response>>>\n", second_message['choices'][0]["message"]["content"], '\n\n')

    # def test_get_current_weather_function(self):
    #     def get_current_weather(location, unit="fahrenheit"):
    #         weather_info = {
    #             "location": location,
    #             "temperature": "7",
    #             "unit": unit,
    #             "forecast": ["sunny", "windy"],
    #         }
    #         return json.dumps(weather_info)

    #     def run_conversation():
    #         # STEP1: モデルにユーザー入力と関数の情報を送る
    #         response = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo-0613",
    #             messages=[{"role": "user", "content": "ボストンの天気はどうなんだろう？"}],
    #             functions=[
    #                 {
    #                     "name": "get_current_weather",
    #                     "description": "指定した場所の現在の天気を取得",
    #                     "parameters": {
    #                         "type": "object",
    #                         "properties": {
    #                             "location": {
    #                                 "type": "string",
    #                                 "description": "都市と州（例：San Francisco, CA)",
    #                             },
    #                             "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
    #                         },
    #                         "required": ["location"],
    #                     },
    #                 }
    #             ],
    #             function_call="auto",
    #         )
    #         message = response["choices"][0]["message"]
    #         print("message>>>\n", message, "\n\n")

    #         if message.get('function_call'):
    #             function_name = message['function_call']['name']
    #             function_response = get_current_weather(
    #                 location=message.get('location'),
    #                 unit=message.get('unit')
    #             )

    #             second_message = openai.ChatCompletion.create(
    #                 model='gpt-3.5-turbo-0613',
    #                 messages=[
    #                     {"role": "user", "content": "ボストンの天気はどうなんだろう？"},
    #                     {'role': 'function', "name": function_name, 'content': function_response}
    #                 ]
    #             )

    #         return second_message

    #     print("response>>>\n", run_conversation()[
    #           "choices"][0]["message"]["content"], "\n\n")
