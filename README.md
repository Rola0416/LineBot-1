# Line Bot + Python 教學 - WMD搞定學院 #

## 1-1 註冊帳號
Github:https://github.com  
Heroku:https://heroku.com

## 1-2 上架範例程式

## 2-1 流程解說
我們可以將Line想像成一個傳遞對話的傳聲筒，  
當使用者傳送文字給我們的Line帳號時，  
程式會收到一個包含使用者ID、他傳送的文字等等的資料，  
然後再根據我們寫的程式去處理這些資料，  
最後回覆使用者。  
而我們回復使用者的程式則要寫在範例程式第35行的handle_message(event)函式中。  
現在我們來看看這段程式：
    def handle_message(event):
        message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(event.reply_token, message)
第一行括號內的引數event是前文所述程式收到的資料，  
裡面包含了
