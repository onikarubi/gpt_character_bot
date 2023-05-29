from .gcp.google_drive_tool import GoogleDriveService

def chat_template_downloader():
    drive = GoogleDriveService(
        target_filename='apis/openai/gpt/templates/hoge.js',
        file_id='1swe1X7Ea7axmhopEf_XzCoxTcNCJNiPZ'
    )

    drive.download()

def chat_template_uploader(target_file: str):
    drive = GoogleDriveService(
        target_filename=target_file, file_id='1xvS8HPN7XrAy2xWlTec1rTM2S1up-V9w')

    drive.upload()
