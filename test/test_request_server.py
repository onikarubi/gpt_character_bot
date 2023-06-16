import uvicorn
import requests
import time

class TestRequestServer:
    def test_request(self):
        response = requests.get('http://0.0.0.0:8000')
        assert response.status_code == 200
        assert response.json()['status'] == 'success'

