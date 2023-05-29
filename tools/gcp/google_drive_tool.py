from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive, GoogleDriveFile
import os

class GoogleDriverAssist:
    """
    GoogleDriverAssist is a utility class for handling errors in Google Drive transactions.
    """
    @classmethod
    def service_transaction(cls, service):
        """
        A decorator to handle exceptions in Google Drive transactions.

        :param service: function to be wrapped
        :return: wrapper function
        """
        def __wrapper(*args, **kwargs):
            try:
                service(*args, **kwargs)

            except:
                raise cls.DriveException('GoogleDrive Function Error')

        return __wrapper

    class DriveException(Exception):
        """
        DriveException is an exception class to be raised in case of Google Drive transaction errors.
        """
        pass


class GoogleDriveLoader:
    """
    GoogleDriveLoader is a base class for handling common functionalities among Google Drive services.
    """
    def __init__(self, target_filename: str, file_id: str = None) -> None:
        """
        Constructor for the GoogleDriveLoader class.

        :param target_filename: filename to be uploaded/downloaded
        :param file_id: id of the file on Google Drive (if known)
        """
        self._target_filename = target_filename
        self._file_id = file_id
        self._g_auth = GoogleAuth()

    @property
    def target_filename(self) -> str:
        """
        Getter for the target filename.

        :return: target filename
        """
        return self._target_filename

    @property
    def file_id(self) -> str:
        """
        Getter for the file id.

        :return: file id
        """
        return self._file_id

    @property
    def g_auth(self) -> GoogleAuth:
        """
        Getter for the GoogleAuth object.

        :return: GoogleAuth object
        """
        return self._g_auth

    def _initialize_drive(self) -> GoogleDrive:
        """
        Initialize the Google Drive service.

        :return: GoogleDrive object
        """
        self.g_auth.CommandLineAuth()
        return GoogleDrive(self._g_auth)

    def _get_google_drive_file(self, file_id: str = '') -> GoogleDriveFile:
        """
        Get a GoogleDriveFile object, either a new one or the one specified by file_id.

        :param file_id: id of the file on Google Drive (if known)
        :return: GoogleDriveFile object
        """
        drive = self._initialize_drive()
        if not file_id:
            return drive.CreateFile()

        return drive.CreateFile({'id': file_id})

    def _get_google_drive_folder(self, file_id = ''):
        drive = self._initialize_drive()
        if not file_id:
            return drive.CreateFile()

        return drive.CreateFile({'parents': [{'id': self.file_id}]})

class GoogleDriveUploader(GoogleDriveLoader):
    """
    GoogleDriveUploader is a class for handling file uploads to Google Drive.
    """
    def __init__(self, target_filename: str, file_id: str = None) -> None:
        super().__init__(target_filename, file_id)

    @GoogleDriverAssist.service_transaction
    def upload(self) -> None:
        """
        Upload a file to Google Drive.

        :return: None
        """
        target_file = self._get_google_drive_folder(self.file_id)
        target_file.SetContentFile(self.target_filename)
        target_file['title'] = os.path.basename(self.target_filename)
        target_file.Upload()


class GoogleDriveDownloader(GoogleDriveLoader):
    """
    GoogleDriveDownloader is a class for handling file downloads from Google Drive.
    """
    def __init__(self, target_filename: str, file_id: str = None) -> None:
        super().__init__(target_filename, file_id)

    @GoogleDriverAssist.service_transaction
    def download(self):
        """
        Download a file from Google Drive.

        :return: None
        """
        target_file = self._get_google_drive_file(file_id=self.file_id)
        target_file.GetContentFile(self.target_filename)


class GoogleDriveService(GoogleDriveLoader):
    """
    GoogleDriveService is a class for providing high-level upload/download functionality using Google Drive.
    """
    def __init__(self, target_filename: str, file_id: str = None) -> None:
        super().__init__(target_filename, file_id)

    def upload(self):
        """
        Upload a file to Google Drive using the GoogleDriveUploader class.

        :return: None
        """
        uploader = GoogleDriveUploader(
            target_filename=self.target_filename,
            file_id=self.file_id
        )
        uploader.upload()

    def download(self):
        """
        Download a file from Google Drive using the GoogleDriveDownloader class.

        :return: None
        """
        downloader = GoogleDriveDownloader(
            target_filename=self.target_filename,
            file_id=self.file_id
        )
        downloader.download()

