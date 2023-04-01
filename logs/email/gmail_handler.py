from email.mime.text import MIMEText
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
import ssl


class SmtpConfig:
    def __init__(self, port: int = 0, host: str='') -> None:
        self._port = port
        self._host = host

    @property
    def port(self): return self._port

    @port.setter
    def port(self, number: float):
        self._port = number

    @property
    def host(self):
        if not self._host:
            return

        return self._host

    @host.setter
    def host(self, host_name: str = ''):
        if not host_name:
            return

        self._host = host_name


class SmtpHandler:
    def __init__(self, smtp_conf: SmtpConfig) -> None:
        self.smtp_conf = smtp_conf
        self._smtp = SMTP(self.smtp_conf.host, self.smtp_conf.port)

    @property
    def smtp(self):
        return self._smtp

    def authentication_smtp(self, email: str = None, password: str = None):
        try:
            context = ssl.create_default_context()
            self.smtp.ehlo()
            self.smtp.starttls(context=context)
            self.smtp.login(user=email, password=password)
            print('認証に成功しました')

        except:
            print('認証に失敗しました')
            raise

        finally:
            self.smtp.quit()


class GmailSender:
    def __init__(self, email: str, password: str, root_email: str = None) -> None:
        self.email = email
        self.password = password

        if root_email:
            self.root_email = root_email

        self.multipart = MIMEMultipart()
        self.smtp_config = SmtpConfig(port=587, host='smtp.gmail.com')
        self.smtp_handler = SmtpHandler(self.smtp_config)
        self.smtp_handler.authentication_smtp(self.email, self.password)

    def send_gmail(self, message: str, subject: str = '', to_email: str = None):
        if not to_email:
            to_email = self.root_email

        self.multipart['From'] = self.email
        self.multipart['To'] = to_email
        self.multipart['Subject'] = subject
        message = MIMEText(message, "plain", "utf-8")
        self.multipart.attach(message)


