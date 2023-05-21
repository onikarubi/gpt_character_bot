from .gcp.upload_google_drive import GoogleDriveUploader

def chat_template_uploader():
    uploader = GoogleDriveUploader(
        filename='apis/openai/gpt/templates/chat_template.csv',
        folder_id='1xvS8HPN7XrAy2xWlTec1rTM2S1up-V9w'
    )

    uploader.upload()

