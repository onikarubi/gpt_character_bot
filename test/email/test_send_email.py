from dotenv import load_dotenv
from logs.email.gmail_handler import GmailSender
import os

class TestGmailSender:
    def test_send_gmail(self):
        load_dotenv('../../.env')
        APPLICATION_BOT_EMAIL = os.getenv('APPLICATION_BOT_EMAIL')
        APPLICATION_BOT_PASSWORD = os.getenv('APPLICATION_BOT_PASSWORD')
        APPLICATION_ROOT_EMAIL = os.getenv('APPLICATION_ROOT_EMAIL')
        gmail_sender = GmailSender(APPLICATION_BOT_EMAIL, APPLICATION_BOT_PASSWORD, APPLICATION_ROOT_EMAIL)

        assert gmail_sender.email == APPLICATION_BOT_EMAIL
        assert gmail_sender.password == APPLICATION_BOT_PASSWORD
        # gmail_sender.send_gmail(
        #     message='test message',
        #     subject='テスト用のメール',
        #     to_email=APPLICATION_ROOT_EMAIL
        # )

        gmail_sender.send_gmail(
            message='test message (to_emailの引数がデフォルト値のケース)',
            subject='to_emailの引数がデフォルト値のケース',
        )

