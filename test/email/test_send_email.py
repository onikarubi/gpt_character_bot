# from dotenv import load_dotenv
# from logs.email.gmail_handler import GmailSender
# import datetime
# import os

# load_dotenv('../../.env')

# class TestGmailSender:
#     APPLICATION_BOT_EMAIL = os.getenv('APPLICATION_BOT_EMAIL')
#     APPLICATION_BOT_PASSWORD = os.getenv('APPLICATION_BOT_PASSWORD')
#     APPLICATION_ROOT_EMAIL = os.getenv('APPLICATION_ROOT_EMAIL')

#     def test_send_gmail(self):
#         gmail_sender = GmailSender(self.APPLICATION_BOT_EMAIL, self.APPLICATION_BOT_PASSWORD, self.APPLICATION_ROOT_EMAIL)

#         assert gmail_sender.email == self.APPLICATION_BOT_EMAIL
#         assert gmail_sender.password == self.APPLICATION_BOT_PASSWORD

#         gmail_sender.send_gmail(
#             message=f'test message (to_emailの引数がデフォルト値のケース)',
#             subject=f'to_emailの引数がデフォルト値のケース: {datetime.datetime.now().ctime()}',
#         )
