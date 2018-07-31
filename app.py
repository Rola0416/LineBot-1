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
        alt_text='天氣模板',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://ananedu.com/a/5/9/images/imge015.jpg',
                    title='板橋區',
                    text='時間\t天氣\t溫度\t濕度\t\n12點\t晴天\t30°\t255\n13點\t晴天\t32°\t200\n14點\t晴天\t28°\t265',
                    actions=[
                        PostbackTemplateAction(
                            label='更改位置',
                            text='postback text1',
                            data='place_change'
                        ),
                        URITemplateAction(
                            label='詳細資料',
                            uri='https://weather.com/weather/today/l/25.02,121.46'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://ananedu.com/a/5/9/images/imge015.jpg',
                    title='台北市',
                    text='時間\t天氣\t溫度\t濕度\t\n12點\t晴天\t30°\t255\n13點\t晴天\t32°\t200\n14點\t晴天\t28°\t265',
                    actions=[
                        PostbackTemplateAction(
                            label='更改位置',
                            text='postback text1',
                            data='place_change'
                        ),
                        URITemplateAction(
                            label='詳細資料',
                            uri='https://weather.com/weather/today/l/25.02,121.46'
                        )
                    ]
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)
    
#@handler.add(PostbackEvent)
#def handle_postback(event):
    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
