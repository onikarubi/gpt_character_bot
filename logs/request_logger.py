from .email.gmail_handler import GmailSender
from dotenv import load_dotenv
import logging
import os

load_dotenv('./.env')

class ApiAccessLogger:
    """
    APIアクセスログを生成するための基本クラス。
    """

    APPLICATION_BOT_EMAIL = os.getenv('APPLICATION_BOT_EMAIL')
    APPLICATION_BOT_PASSWORD = os.getenv('APPLICATION_BOT_PASSWORD')
    APPLICATION_ROOT_EMAIL = os.getenv('APPLICATION_ROOT_EMAIL')

    def __init__(self, output_filename: str, level: int, file_output: bool = True, console: bool = True, send_email: bool = False) -> None:
        self.output_filename = output_filename
        self.level = level
        self.file_output = file_output
        self.console = console
        self.send_email = send_email
        self.log_file = os.path.join('logs', f"{output_filename}.log")
        self.file_handler = logging.FileHandler(self.log_file)
        self.stream_handler = logging.StreamHandler()
        self.format = logging.Formatter('%(levelname)s: %(message)s')
        self.file_handler.setFormatter(self.format)
        self.stream_handler.setFormatter(self.format)
        self.logger = logging.getLogger(__name__)
        self._logger_init()

    def _config_formatter(self) -> logging.Formatter:
        if self.level == logging.INFO:
            return logging.Formatter('%(levelname)s: %(message)s')

        elif self.level == logging.DEBUG:
            return logging.Formatter('%(asctime)s  %(levelname)s: %(module)s %(message)s')

        elif self.level == logging.ERROR:
            return logging.Formatter('%(asctime)s  %(levelname)s: %(module)s %(message)s')

        else:
            raise ValueError('ログレベルを適切に指定してください')

    def logger_output(self, message: str):
        """
        与えられたメッセージをログに出力する。
        """

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
        """
        与えられたメッセージをメールで送信する。
        """

        if not self.send_email: return

        gmail_handler = GmailSender(
            email=self.APPLICATION_BOT_EMAIL,
            password=self.APPLICATION_BOT_PASSWORD,
            root_email=self.APPLICATION_ROOT_EMAIL
            )

        gmail_handler.send_gmail(msg)

    def _logger_init(self):
        """
        ロガーの初期設定を行う。
        """

        self.logger.setLevel(self.level)

        if self.file_output:
            self.logger.addHandler(self.file_handler)

        if self.console:
            self.logger.addHandler(self.stream_handler)


class LoggerInfo(ApiAccessLogger):
    """
    INFOレベルのログを生成するクラス。
    """

    def __init__(self, output_filename: str, level: int = logging.INFO, file_output: bool = True, console: bool = True, send_email: bool = False) -> None:
        super().__init__(output_filename, level, file_output, console, send_email)
        self.level = level
        self.console = True
        self.file_output = True
        self.send_email = False


class LoggerDebug(ApiAccessLogger):
    """
    DEBUGレベルのログを生成するクラス。
    """

    def __init__(self, output_filename: str, level: int = logging.DEBUG, file_output: bool = True, console: bool = True, send_email: bool = False) -> None:
        super().__init__(output_filename, level, file_output, console, send_email)
        self.level = level
        self.console = True
        self.file_output = False
        self.send_email = False


class LoggerError(ApiAccessLogger):
    """
    ERRORレベルのログを生成するクラス。
    """

    def __init__(self, output_filename: str, level: int = logging.ERROR, file_output: bool = True, console: bool = True, send_email: bool = False) -> None:
        super().__init__(output_filename, level, file_output, console, send_email)
        self.level = level
        self.file_output = True
        self.console = True
        self.send_email = True


def logger_output(level: str = '', message: str = '', output_filename: str = ''):
    """
    与えられたログレベル、メッセージ、および出力ファイル名を使用して、ログを出力する。

    :param level: ログレベル（'info', 'debug', 'error'のいずれか）
    :param message: ログに出力するメッセージ
    :param output_filename: ログを出力するファイル名
    """

    if not level or not message: return
    if not level in ['info', 'debug', 'error']:
        return

    if level == 'info':
        logger = LoggerInfo(output_filename=output_filename)

    elif level == 'debug':
        logger = LoggerDebug(output_filename=output_filename)

    elif level == 'error':
        logger = LoggerError(output_filename=output_filename)

    logger.logger_output(message)

