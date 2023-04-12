from fastapi.testclient import TestClient
from linebot.models import TextMessage, MessageEvent, TextSendMessage, ImageSendMessage
from main import app, handle_message_text
from dotenv import load_dotenv
from pytest_mock import MockerFixture
import json

load_dotenv('./.env')

client = TestClient(app)

def test_callback(mocker: MockerFixture):
    client = TestClient(app)
    mocker.patch("linebot.SignatureValidator.validate", return_value=True)
    data = {"events": [{"replyToken": "dummy_token",
                        "message": {"text": "Hello, test."}, "type": "text"}]}
    response = client.post("/callback", json=data)
    assert response.status_code == 200
    assert response.json()['content'] == json.dumps(data)


def test_callback_reply_text(mocker: MockerFixture):
    event = MessageEvent(
        reply_token='dummy_token',
        message=TextMessage(text='sample_text'),
    )
    reply_mock = mocker.Mock()
    mocker.patch("linebot.LineBotApi.reply_message",
                 reply_mock)
    handle_message_text(event)

    reply_mock.assert_called()
    reply_mock.assert_called_once()
    reply_mock.assert_called_with(
        reply_token=event.reply_token, messages=TextSendMessage(text=event.message.text))


def test_callback_reply_image(mocker: MockerFixture):
    event = MessageEvent(
        reply_token='dummy_token',
        message=TextMessage(text='猫の画像'),
    )
    reply_mock = mocker.Mock()
    mocker.patch("linebot.LineBotApi.reply_message", reply_mock)
    handle_message_text(event, test_mode=True)

    reply_mock.assert_called()
    reply_mock.assert_called_once()
    reply_mock.assert_called_once_with(
        reply_token=event.reply_token,
        messages=ImageSendMessage(
            original_content_url='dummy_original_content_url',
            preview_image_url='dummy_preview_image_url'
        )
    )




