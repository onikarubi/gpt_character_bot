from fastapi import FastAPI, Request, Response, status
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import TextMessage, MessageEvent
from apis.linebot.linebot import LineBotReplyText, LineBotHandler
from apis.openai.gpt.conversion_bot import ConversionBot
from apis.openai.gpt.langchains.llm_chains import SearchQuestionAndAnswer
import logs.request_logger
import os
import uvicorn

LINE_BOT_API_TOKEN = os.getenv('LINE_BOT_API_TOKEN')
LINE_BOT_API_SECRET = os.getenv('LINE_BOT_API_SECRET')

app = FastAPI()

line_bot_handler = LineBotHandler(
    api_token=LINE_BOT_API_TOKEN,
    api_secret=LINE_BOT_API_SECRET
)

@app.post('/callback')
async def callback(request: Request):
    signature = request.headers.get('X-Line-Signature')
    body = await request.body()

    try:
        line_bot_handler.webhook_handler.handle(body.decode(encoding='utf-8'), signature)

    except InvalidSignatureError:
        logs.request_logger.logger_output(level='error', message=f'署名に失敗しました: {callback}', file_output='line_api_access')
        raise

    except AttributeError:
        logs.request_logger.logger_output(
            level='error', message=f'署名に失敗しました: {callback}\n署名の設定を見直して下さい')
        raise

    return {"status_code": Response(status_code=status.HTTP_200_OK), "content": body}


def reply_message_text(event: MessageEvent):
    conversion_character = ConversionBot()
    response_content = conversion_character(event.message.text)
    reply_message = LineBotReplyText(
        api_token=LINE_BOT_API_TOKEN,
        api_secret=LINE_BOT_API_SECRET,
        text_content=response_content
    )

    reply_message.reply_message(event)


@line_bot_handler.webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message_text(event: MessageEvent):
    try:
        reply_message_text(event)

    except:
        error_msg = 'Line bot上で問題が発生しました。'
        raise LineBotApiError(error_msg)

if __name__ == '__main__':
    q_and_a = SearchQuestionAndAnswer(question_prompt='現在日本の総理大臣は誰ですか？')
    q_and_a.run()
    # uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
