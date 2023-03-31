from dotenv import load_dotenv
import os

class ConfigEnvironment:
    def __init__(self) -> None:
        self._line_bot_api_token = None
        self._line_bot_api_secret = None
        self._load_config()

    def _load_config(self):
        self._line_bot_api_token = os.getenv('LINE_BOT_API_TOKEN')
        self._line_bot_api_secret = os.getenv('LINE_BOT_API_SECRET')

        if not self._line_bot_api_secret or not self._line_bot_api_token:
            load_dotenv('./.env')
            self._line_bot_api_token = os.getenv('LINE_BOT_API_TOKEN')
            self._line_bot_api_secret = os.getenv('LINE_BOT_API_SECRET')

    @property
    def get_api_token(self):
        return self._line_bot_api_token

    @property
    def get_api_secret(self):
        return self._line_bot_api_secret
