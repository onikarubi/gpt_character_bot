import requests
import pytest

is_run_server = False
class TestRequestServer:

    @pytest.mark.skipif(is_run_server == False, reason='If the server is running, run')
    def test_request(self):
        response = requests.get('http://0.0.0.0:8000')
        assert response.status_code == 200
        assert response.json()['status'] == 'success'

