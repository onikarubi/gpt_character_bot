from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, ImageSendMessage, TextSendMessage
from linebot.exceptions import LineBotApiError


class LineBotHandler:
    def __init__(self, api_token=None, api_secret=None) -> None:
        self._api_token = api_token
        self._api_secret = api_secret
        self._line_bot_api = LineBotApi(self._api_token)
        self._webhook_handler = WebhookHandler(self._api_secret)

    @property
    def line_bot_api(self):
        if not self._api_token:
            raise ValueError('api tokenが指定されていません')
        return self._line_bot_api

    @property
    def webhook_handler(self):
        if not self._api_secret:
            raise ValueError('api secretが指定されていません')
        return self._webhook_handler



class LineBotReplyText(LineBotHandler):
    def __init__(self, api_token=None, api_secret=None, text_content=None) -> None:
        super().__init__(api_token, api_secret)
        self.text_content = text_content

    def reply_message(self, message_event: MessageEvent):
        send_text = self._send_text_message(message_event)

        self.line_bot_api.reply_message(
            reply_token=message_event.reply_token,
            messages=send_text
        )

    def _send_text_message(self, event: MessageEvent) -> TextSendMessage:
        if not self.text_content:
            return TextSendMessage(event.message.text)

        return TextSendMessage(self.text_content)


class LineBotReplyImage(LineBotHandler):
    def __init__(self, api_token=None, api_secret=None, test_mode=False, image_size: int = 512) -> None:
        super().__init__(api_token, api_secret)
        self.test_mode = test_mode
        self.image_size = image_size

    def reply_message(self, event: MessageEvent):
        if not event.message.text == "猫の画像":
            return

        message_image = self._create_image(event)
        self._line_bot_api.reply_message(
            reply_token=event.reply_token,
            messages=message_image
        )


