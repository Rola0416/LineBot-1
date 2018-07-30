from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('vlgEBYCHqjedWeOr0LghZpXN7KALtdXebquusc3WHQOPBwEGujQZ0c/fbA51Kb4kyHvJ335W8D35WeORu7i26jnjYK7T4Nuf5jLhZvByrEnIDggnhcbT1Jdaw6b5TWsrfIiGn3XKuvNHn3z1yVE9lQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('dfaf82e2cd7fae694b3d6fc9bc691dac')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        thumbnail_image_url='https://cc.tvbs.com.tw/img/program/upload/2018/03/05/20180305124010-4c9c5715.jpg',
        title='Menu',
        text='我帥嗎',
        actions=[
            PostbackTemplateAction(
                label='蠻帥的',
                data='good'
            ),
            MessageTemplateAction(
                label='還好',
                text='我覺得普通'
            ),
            URITemplateAction(
                label='不行',
                uri='http://cdn.clickme.net/Gallery/2017/08/03/2c04861ba0c20c428572205919b0f127.jpg'
            )
        ]
    )
)
line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'good':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='真棒'))
    elif event.postback.data == 'bad':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='喔是喔'))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
