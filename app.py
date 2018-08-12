from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests

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

#user類別
class user:
    def __init__(self,Name,ID,Status):
        self.Name = Name
        self.ID = ID
        self.Status = Status

#讀取成員名單
def GetUserList():
    url = "https://script.google.com/macros/s/AKfycbwVs2Si91yKz6m3utpaPtsttbh_lUQ8LOQM3Zud2hPFxXCgW3u1/exec"
    payload = {
        'sheetUrl':"https://docs.google.com/spreadsheets/d/118ZANXoqpYW9BA5MTr58QsWKt1ZkxIphVRS6tZ3dzqo/edit#gid=0",
        'sheetTag':"成員列表",
        'row': 2,
        'col': 1,
        'endRow' : 51,
        'endCol' : 20
    }
    resp = requests.get(url, params=payload)
    temp = resp.text.split(',')
    userlist = []
    i = 0
    while i < len(temp):
        if temp[i] != "":
            userlist.append(user(temp[i],temp[i+1],temp[i+2]))
            i+=3
        else:
            break
    return userlist

def Login(user_id,userlist):
    for user in userlist:
        if user.ID == user_id:
            return userlist.index(user)
    return -1

def Signup(index,text):
    if index < 0:
        url = "https://script.google.com/macros/s/AKfycbxn7Slc2_sKHTc6uEy3zmm3Bh_4duiGCXLavUM3RB0a3yzjAxc/exec"
        payload = {
            'sheetUrl':"https://docs.google.com/spreadsheets/d/118ZANXoqpYW9BA5MTr58QsWKt1ZkxIphVRS6tZ3dzqo/edit#gid=0",
            'sheetTag':"成員列表",
            'type':'add'
            'data':'none000,'+text+',學生'
        }
        requests.get(url, params=payload)
    else:
        url = "https://script.google.com/macros/s/AKfycbxn7Slc2_sKHTc6uEy3zmm3Bh_4duiGCXLavUM3RB0a3yzjAxc/exec"
        payload = {
            'sheetUrl':"https://docs.google.com/spreadsheets/d/118ZANXoqpYW9BA5MTr58QsWKt1ZkxIphVRS6tZ3dzqo/edit#gid=0",
            'sheetTag':"成員列表",
            'type':'change'
            'x':index
            'y':1
            'data':text
        }
        requests.get(url, params=payload)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        userlist = GetUserList()
        clientindex = Login(event.source.user_id)
        if clientindex > -1:
            if userlist[clientindex].Name != 'none000':
                #開始使用功能
            else:
                Signup(clientindext,event.message.text)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='註冊成功!歡迎您~'))
        else:
            Signup(clientindext,event.source.user_id)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='初次使用，請輸入您的姓名'))
            
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="發生錯誤01"))
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
