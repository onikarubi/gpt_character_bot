from fastapi.testclient import TestClient
from linebot import LineBotApi
from linebot.models import TextMessage, MessageEvent, TextSendMessage
from main import app, handle_message
from dotenv import load_dotenv
from pytest_mock import MockerFixture
import os
import json

load_dotenv('./.env')

client = TestClient(app)


def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}
    print(response.json())

def test_callback(mocker: MockerFixture):
    client = TestClient(app)
    mocker.patch("linebot.SignatureValidator.validate", return_value=True)
    data = {"events": [{"replyToken": "dummy_token",
                        "message": {"text": "Hello, test."}, "type": "text"}]}
    response = client.post("/callback", json=data)
    assert response.status_code == 200
    assert response.json()['content'] == json.dumps(data)


def test_callback_handler(mocker: MockerFixture):
    event = MessageEvent(
        reply_token='dummy_token',
        message=TextMessage(text='sample_text'),
    )
    mock_line_bot_api = mocker.Mock()
    mocker.patch("linebot.LineBotApi.reply_message", mock_line_bot_api)
    handle_message(event)

    mock_line_bot_api.assert_called()
    mock_line_bot_api.assert_called_once()
    mock_line_bot_api.assert_called_with(event.reply_token, messages=TextSendMessage(text=event.message.text))




