from .gcp.google_drive_tool import GoogleDriveService
from .chat.chat_application import ChatCommandLineApplication
from abc import ABCMeta, abstractstaticmethod
import uvicorn
import os
import subprocess


class CliService(metaclass=ABCMeta):
    @abstractstaticmethod
    def execute(self):
        pass


class DriveToolService(CliService):
    DRIVE_ENVFILE_ID = os.getenv('DRIVE_ENVFILE_ID')
    DRIVE_CHAT_TEMPLATEFILE_ID = os.getenv('DRIVE_CHAT_TEMPLATEFILE_ID')
    DRIVE_UPLOAD_FOLDER_ID = os.getenv('DRIVE_UPLOAD_FOLDER_ID')

    def execute(self):
        print('Please select drive service\n')
        print('1, Upload local files to drive  2, download from drive folder')
        selector = int(input('select mode >> '))
        drive_service = self._drive_config_service()

        if selector == 1:
            drive_service.upload()

        elif selector == 2:
            print(drive_service)
            drive_service.download()

        else:
            print('Sorry please try again.')

    def _drive_config_service(self) -> GoogleDriveService:
        print('1, .env file  2, chat_template_file  3, other')
        selector = int(input('select mode >> '))
        if selector == 1:
            target_filename = '.env'
            file_id = self.DRIVE_ENVFILE_ID

        elif selector == 2:
            target_filename = "apis/openai/gpt/templates/chat_template.csv"
            file_id = self.DRIVE_CHAT_TEMPLATEFILE_ID

        else:
            print('Sorry, we are in the process of preparing.')
            return

        return GoogleDriveService(target_filename, file_id=file_id, folder_id=self.DRIVE_UPLOAD_FOLDER_ID)


class ApplicationService(CliService):
    chat_cli: ChatCommandLineApplication

    def execute(self):
        print('1, start uvicorn server  2, start cli chat (debug)  3, chat cli 4, streamlit app start')
        selector = int(input('select mode >> '))

        if selector == 1:
            uvicorn.run('main:app', host='0.0.0.0', reload=True)

        elif selector == 2:
            self.chat_cli = ChatCommandLineApplication(debug=True)
            self.chat_cli.conversation()

        elif selector == 3:
            self.chat_cli = ChatCommandLineApplication(debug=False)
            self.chat_cli.conversation()

        elif selector == 4:
            subprocess.call(['streamlit', 'run', 'chat.py', '--server.port=8000', '--server.address=0.0.0.0'])


class CommandLineExecutor:
    cli_service: CliService

    def execute_cli(self):
        print('1, application start  2, drive tool  3, exit cli')
        selector = int(input('select mode >> '))

        if selector == 1:
            self.cli_service = ApplicationService()

        elif selector == 2:
            self.cli_service = DriveToolService()

        else:
            print('exit cli')
            return

        self.cli_service.execute()
