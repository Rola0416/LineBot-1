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

#-----------函數區-------------



#-----------------------------

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
        alt_text='天氣模板',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://ananedu.com/a/5/9/images/imge015.jpg',
                    title='12:00',
                    text='晴天\n溫度：30.5°\n濕度；223',
                    actions=[
                        URITemplateAction(
                            label='詳細資料',
                            uri='https://weather.com/weather/today/l/25.02,121.46?par=google'
                        ),
                        PostbackTemplateAction(
                            label='變更位置',
                            data='place_change'
                        )
                    ]
                )
                CarouselColumn(
                    title='13:00',
                    text='雨天\n溫度：22°\n濕度；1005',
                    actions=[
                        URITemplateAction(
                            label='詳細資料',
                            uri='https://weather.com/weather/today/l/25.02,121.46?par=google'
                        ),
                        PostbackTemplateAction(
                            label='變更位置',
                            data='place_change'
                        )
                    ]
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)
    
@handler.add(PostbackEvent)
def handle_postback(event):
    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
