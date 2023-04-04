from .email.gmail_handler import GmailSender
from dotenv import load_dotenv
import logging
import os

load_dotenv('./.env')

class LineApiAccessLogger:

    APPLICATION_BOT_EMAIL = os.getenv('APPLICATION_BOT_EMAIL')
    APPLICATION_BOT_PASSWORD = os.getenv('APPLICATION_BOT_PASSWORD')
    APPLICATION_ROOT_EMAIL = os.getenv('APPLICATION_ROOT_EMAIL')

    def __init__(self, level: int, file_output: bool = True, console: bool = True, send_email: bool = False) -> None:
        self.level = level
        self.file_output = file_output
        self.console = console
        self.send_email = send_email
        self.log_file = os.path.join('logs', "line_api_access.log")
        self.file_handler = logging.FileHandler(self.log_file)
        self.stream_handler = logging.StreamHandler()
        self.format = logging.Formatter('%(levelname)s: %(message)s')
        self.file_handler.setFormatter(self.format)
        self.stream_handler.setFormatter(self.format)
        self.logger = logging.getLogger(__name__)
        self._logger_init()

    def logger_output(self, message: str):
        if self.level == logging.INFO:
            self.logger.info(message)

        elif self.level == logging.DEBUG:
            self.logger.debug(message)

        elif self.level == logging.ERROR:
            self.logger.error(message)

        else:
            raise ValueError('ログレベルを適切に指定してください')

        if not self.send_email: return
        self._send_email(message)


    def _send_email(self, msg: str):
        if not self.send_email: return

        gmail_handler = GmailSender(
            email=self.APPLICATION_BOT_EMAIL,
            password=self.APPLICATION_BOT_PASSWORD,
            root_email=self.APPLICATION_ROOT_EMAIL
            )

        gmail_handler.send_gmail(msg)

    def _logger_init(self):
        self.logger.setLevel(self.level)

        if self.file_output:
            self.logger.addHandler(self.file_handler)

        if self.console:
            self.logger.addHandler(self.stream_handler)


class LoggerInfo(LineApiAccessLogger):
    def __init__(self, level: int = logging.INFO, file_output: bool = True, console: bool = True, send_email: bool = False) -> None:
        super().__init__(level, file_output, console, send_email)
        self.level = level
        self.console = True
        self.file_output = True
        self.send_email = False


class LoggerDebug(LineApiAccessLogger):
    def __init__(self, level: int = logging.DEBUG, file_output: bool = True, console: bool = True, send_email: bool = False) -> None:
        super().__init__(level, file_output, console, send_email)
        self.level = level
        self.console = True
        self.file_output = False
        self.send_email = False


class LoggerError(LineApiAccessLogger):
    def __init__(self, level: int = logging.ERROR, file_output: bool = True, console: bool = True, send_email: bool = False) -> None:
        super().__init__(level, file_output, console, send_email)
        self.level = level
        self.file_output = True
        self.console = True
        self.send_email = True


def line_logger_output(level: str = '', message: str = ''):
    if not level or not message: return
    if not level in ['info', 'debug', 'error']:
        return

    if level == 'info':
        logger = LoggerInfo()

    elif level == 'debug':
        logger = LoggerDebug()

    elif level == 'error':
        logger = LoggerError()

    logger.logger_output(message)

