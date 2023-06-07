from .gcp.google_drive_tool import GoogleDriveService
from apis.openai.gpt.langchains.llm_chains import SearchQuestionAndAnswer
from abc import ABCMeta, abstractstaticmethod
import uvicorn
import os


class CliService(metaclass=ABCMeta):
    @abstractstaticmethod
    def execute_service(self):
        pass


class DriveToolService(CliService):
    DRIVE_ENVFILE_ID = os.getenv('DRIVE_ENVFILE_ID')
    DRIVE_CHAT_TEMPLATEFILE_ID = os.getenv('DRIVE_CHAT_TEMPLATEFILE_ID')
    DRIVE_UPLOAD_FOLDER_ID = os.getenv('DRIVE_UPLOAD_FOLDER_ID')

    def execute_service(self):
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
    def execute_service(self):
        print('1, start uvicorn server  2, start cli chat (debug mode)  3 or other, start chat cli')
        selector = int(input('select mode >> '))

        if selector == 1:
            uvicorn.run('main:app', host='0.0.0.0', reload=True)

        elif selector == 2:
            self._chat_command_line(debug=True)

        else:
            self._chat_command_line()

    def _chat_command_line(self, debug: bool = False):
        print('Lets take start!')
        question = input('user >> ')
        app = SearchQuestionAndAnswer(is_verbose=debug)

        while True:
            response = app.run(prompt=question)
            print(response)
            question = input('user >> ')

            if question == 'exit':
                print('exit chat !!')
                break

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

        self.cli_service.execute_service()
