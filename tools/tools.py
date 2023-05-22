from .gcp.google_drive_tool import GoogleDriveService

def chat_template_uploader():
    drive = GoogleDriveService(
        filename='apis/openai/gpt/templates/hoge.js',
        folder_id='1xvS8HPN7XrAy2xWlTec1rTM2S1up-V9w'
    )

    drive.upload()

