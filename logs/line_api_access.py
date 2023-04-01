import logging
import os


class LineApiAccessLogger:
    def __init__(self, level: int = logging.INFO, file_output: bool = True, console: bool = True, send_email: bool = False) -> None:
        self.level = level
        self.file_output = file_output
        self.console = console
        self.send_email = send_email
        self.log_file = os.path.json('logs', "line_api_access.log")
        self.file_handler = logging.FileHandler(self.log_file)
        self.stream_handler = logging.StreamHandler()
        self.format = logging.Formatter('%(levelname)s: %(message)s')
        self.file_handler.setFormatter(self.format)
        self.stream_handler.setFormatter(self.format)
        self.logger = logging.getLogger(__name__)


    def message_handler(self, message: str):
        self.logger.setLevel(self.level)

        if self.file_output:
            self.logger.addHandler(self.file_handler)

        if self.console:
            self.logger.addHandler(self.stream_handler)

        self.logger.info(message)

    def send_email(self, error_msg: str):
        pass


class LoggerInfo(LineApiAccessLogger):
    def __init__(self, level: int = logging.INFO, file_output: bool = True, console: bool = True, send_email: bool = False) -> None:
        super().__init__(level, file_output, console, send_email)
        self.level = logging.INFO
        self.console = True
        self.file_output = True
        self.send_email = False


class LoggerDebug(LineApiAccessLogger):
    def __init__(self, level: int = logging.INFO, file_output: bool = True, console: bool = True, send_email: bool = False) -> None:
        super().__init__(level, file_output, console, send_email)
        self.level = logging.DEBUG
        self.console = True
        self.file_output = False
        self.send_email = False


class LoggerError(LineApiAccessLogger):
    def __init__(self, level: int = logging.INFO, file_output: bool = True, console: bool = True, send_email: bool = False) -> None:
        super().__init__(level, file_output, console, send_email)
        self.level = logging.ERROR
        self.file_output = True
        self.console = True
        self.send_email = True





