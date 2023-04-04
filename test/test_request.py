import requests
import pytest

class TestLineMessagingApi:

    def test_line_messaging_api_request_callback(self):
        response = requests.get('http://127.0.0.1:8000')
        assert response.status_code == 200


