from .gcp.google_drive_tool import GoogleDriveService

def chat_template_uploader():
    drive = GoogleDriveService(
        target_filename='apis/openai/gpt/templates/hoge.js',
        file_id='1swe1X7Ea7axmhopEf_XzCoxTcNCJNiPZ'
    )

    drive.download()



