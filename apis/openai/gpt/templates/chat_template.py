import csv

class ChatTemplate:
    def __init__(self, csv_path) -> None:
        self.csv_path = csv_path
        self._templates = self._read_chat_templates()

    def _read_chat_templates(self) -> list[dict[str, str]]:
        with open(self.csv_path) as csv_file:
            templates = csv.DictReader(csv_file)

            return [template for template in templates]

    @property
    def templates(self) -> list[dict[str, str]]:
        if len(self._templates) < 1:
            raise IndexError('templatesの中身が空です')

        return self._templates

