from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

class GoogleDriveUploader:
    def __init__(self, filename: str, folder_id: str = None) -> None:
        self.filename = filename
        self.folder_id = folder_id
        self.g_auth = GoogleAuth()
        self.drive = self._get_initialize_drive()

        if self.folder_id:
            self.target = self.drive.CreateFile({"parents": [{'id': folder_id}]})

        else:
            self.target = self.drive.CreateFile()

    def _get_initialize_drive(self) -> GoogleDrive:
        self.g_auth.CommandLineAuth()
        return GoogleDrive(self.g_auth)

    def upload(self) -> None:
        try:
            self.target.SetContentFile(self.filename)
            self.target['title'] = os.path.basename(self.filename)
            self.target.Upload()
            print(self.target)

        except:
            raise





