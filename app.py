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
line_bot_api = LineBotApi('LYU17p/05jfJVP9/qFJSDy9UehswxFb+lJr9B1RBC4yu8Btp8e5bUZVRqZAsBm/21u/OfjxDt/HkObxp1LCsv43q1+wqvsOnLML4EGYKJrnLv0X1qEMvsjCxZPm2spLSs/ygc6zYVDE62F5/gT3YXwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('ac6df3f9df4d72cdf75eda9d0a7ae488')

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
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
