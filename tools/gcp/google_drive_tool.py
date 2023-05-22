from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive, GoogleDriveFile
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
    def __init__(self, target_filename: str, file_id: str = None) -> None:
        self._target_filename = target_filename
        self._file_id = file_id
        self._g_auth = GoogleAuth()

    @property
    def target_filename(self) -> str:
        return self._target_filename

    @property
    def file_id(self) -> str:
        return self._file_id

    @property
    def g_auth(self) -> GoogleAuth:
        return self._g_auth

    def _initialize_drive(self) -> GoogleDrive:
        self.g_auth.CommandLineAuth()
        return GoogleDrive(self._g_auth)

    def _get_google_drive_file(self, file_id: str = '') -> GoogleDriveFile:
        drive = self._initialize_drive()
        if not file_id:
            return drive.CreateFile()

        return drive.CreateFile({'id': file_id})


class GoogleDriveUploader(GoogleDriveLoader):
    def __init__(self, target_filename: str, file_id: str = None) -> None:
        super().__init__(target_filename, file_id)

    @GoogleDriverAssist.service_transaction
    def upload(self) -> None:
        target_file = self._get_google_drive_file(self.file_id)
        target_file.SetContentFile(self.target_filename)
        target_file['title'] = os.path.basename(self.target_filename)
        target_file.Upload()
        print(self.target)


class GoogleDriveDownloader(GoogleDriveLoader):
    def __init__(self, target_filename: str, file_id: str = None) -> None:
        super().__init__(target_filename, file_id)

    @GoogleDriverAssist.service_transaction
    def download(self):
        target_file = self._get_google_drive_file(file_id=self.file_id)
        target_file.GetContentFile(self.target_filename)


class GoogleDriveService(GoogleDriveLoader):
    def __init__(self, target_filename: str, file_id: str = None) -> None:
        super().__init__(target_filename, file_id)

    def upload(self):
        uploader = GoogleDriveUploader(
            target_filename=self.target_filename,
            file_id=self.file_id
        )
        uploader.upload()

    def download(self):
        downloader = GoogleDriveDownloader(
            target_filename=self.target_filename,
            file_id=self.file_id
        )

        downloader.download()


