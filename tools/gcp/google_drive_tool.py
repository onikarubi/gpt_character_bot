from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

class GoogleDriverAssist:
    @classmethod
    def service_transaction(cls, service):
        def __wrapper(*args, **kwargs):
            try:
                service(*args, **kwargs)

            except:
                raise cls.DriveException('GoogleDrive Function Error')

        return __wrapper

    class DriveException(Exception):
        pass


class GoogleDriveLoader:
    def __init__(self, target_filename: str, folder_id: str = None) -> None:
        self._target_filename = target_filename
        self._folder_id = folder_id
        self._g_auth = GoogleAuth()

    @property
    def target_filename(self):
        return self._target_filename

    @property
    def folder_id(self):
        return self._folder_id

    @property
    def g_auth(self):
        return self._g_auth

    def _initialize_drive(self) -> GoogleDrive:
        self._g_auth.CommandLineAuth()
        return GoogleDrive(self._g_auth)


class GoogleDriveUploader(GoogleDriveLoader):
    def __init__(self, target_filename: str, folder_id: str = None) -> None:
        super().__init__(target_filename, folder_id)
        self.drive = self._initialize_drive()

        if self.folder_id:
            self.target = self.drive.CreateFile({"parents": [{'id': folder_id}]})

        else:
            self.target = self.drive.CreateFile()

    @GoogleDriverAssist.service_transaction
    def upload(self) -> None:
        self.target.SetContentFile(self.target_filename)
        self.target['title'] = os.path.basename(self.target_filename)
        self.target.Upload()
        print(self.target)


class GoogleDriveDownloader(GoogleDriveLoader):
    def __init__(self, target_filename: str, folder_id: str = None) -> None:
        super().__init__(target_filename, folder_id)

    def download(self): pass


class GoogleDriveService(GoogleDriveLoader):
    def __init__(self, target_filename: str, folder_id: str = None) -> None:
        super().__init__(target_filename, folder_id)

    def upload(self):
        uploader = GoogleDriveUploader(
            target_filename=self.target_filename,
            folder_id=self.folder_id
        )
        uploader.upload()

    def download(self):
        pass


