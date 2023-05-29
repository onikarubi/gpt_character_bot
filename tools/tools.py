from .gcp.google_drive_tool import GoogleDriveService
from apis.openai.gpt.langchains.llm_chains import SearchQuestionAndAnswer
from abc import ABCMeta, abstractstaticmethod
import uvicorn
import os

class ChatToolService(metaclass=ABCMeta):
    @abstractstaticmethod
    def execute_service(self):
        pass

class DriveToolService(ChatToolService):
    def execute_service(self):
        print('Please select drive service\n')
        print('1, Upload local files to drive  2, download from drive folder')
        selector = int(input('select mode >> '))

        if selector == 1:
            self._chat_template_uploader()

        elif selector == 2:
            self._chat_template_downloader()

        else:
            print('Sorry please try again.')

    def _chat_template_uploader(self):
        print('1, .env file  2, other')
        selector = int(input('select mode >> '))

        if not selector == 1:
            print('Sorry, we are in the process of preparing.')

        drive = GoogleDriveService(
        target_filename='.env',
        file_id=os.getenv('DEFAULT_DRIVE_UPLOAD_FOLDER_ID')
    )
        drive.upload()

    def _chat_template_downloader(self):
        print('1, .env file  2, other')
        selector = int(input('select mode >> '))
        if not selector == 1:
            print('Sorry, we are in the process of preparing.')

        drive = GoogleDriveService(target_filename='.env', file_id=os.getenv('DRIVE_ENV_FILE_DOWNLOAD_ID'))
        drive.download()


class ApplicationToolService(ChatToolService):
    def execute_service(self):
        print('1, start uvicorn server  2, start cli chat (debug mode)  3 or other, start chat cli')
        selector = int(input('select mode >> '))

        if selector == 1:
            uvicorn.run('main:app', host='0.0.0.0', reload=True)
        elif selector == 2:
            self._chat_command_line(debug=True)

        else:
            self._chat_command_line()

    def _chat_command_line(self, debug: bool=False):
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


class ChatToolsController:
    tool_service: ChatToolService

    def execute_controller(self):
        print('1, application start  2, drive tool  3, exit cli')
        selector = int(input('select mode >> '))

        if selector == 1:
            self.tool_service = ApplicationToolService()

        elif selector == 2:
            self.tool_service = DriveToolService()

        else:
            print('exit cli')
            return

        self.tool_service.execute_service()

