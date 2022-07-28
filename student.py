import os

import requests
from boto.s3.connection import S3Connection
from bs4 import BeautifulSoup as BS4
from fake_useragent import UserAgent
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = Flask(__name__)

department_number = {
    '法律': '71', '法學': '712', '司法': '714', '財法': '716',
    '公行': '72',
    '經濟': '73',
    '社會': '74', '社學': '742', '社工': '744',
    '財政': '75',
    '不動': '76',
    '會計': '77',
    '統計': '78',
    '企管': '79',
    '金融': '80',
    '中文': '81',
    '應外': '82',
    '歷史': '83',
    '休運': '84',
    '資工': '85',
    '通訊': '86',
    '電機': '87'
}

department_name = {v: k for k, v in department_number.items()}

s3 = S3Connection(os.environ['LINE_CHANNEL_ACCESS_TOKEN'], os.environ['LINE_CHANNEL_SECRET'])
line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if isinstance(event, MessageEvent):
        if event.message.text in department_name.keys():
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=department_name[event.message.text] + '系'))
        elif event.message.text.strip('系') in department_number.keys():
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=department_number[event.message.text.strip('系')]))
        elif event.message.text.isdecimal() and event.message.text[0] in ['3', '4', '7']:
            header = {"user-agent": UserAgent().random}
            url = "http://lms.ntpu.edu.tw/portfolio/search.php?fmScope=2&fmKeyword=" + event.message.text
            web = requests.get(url, headers=header)
            web.encoding = "utf-8"

            html = BS4(web.text, "html.parser")
            name = html.find("div", {"class": "bloglistTitle"})

            if name is None:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="學號" + event.message.text + "不存在"))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=name.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
