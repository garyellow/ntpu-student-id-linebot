import requests
from bs4 import BeautifulSoup as BS4
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from fake_useragent import UserAgent
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

department_number = {
    '法律': 71, '法學': 712, '司法': 714, '財法': 716,
    '公行': 72,
    '經濟': 73,
    '社會': 74, '社學': 742, '社工': 744,
    '財政': 75,
    '不動': 76,
    '會計': 77,
    '統計': 78,
    '企管': 79,
    '金融': 80,
    '中文': 81,
    '應外': 82,
    '歷史': 83,
    '休運': 84,
    '資工': 85,
    '通訊': 86,
    '電機': 87
}

department_name = {v: k for k, v in department_number.items()}

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == "POST":
        message = []

        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")

        message.append(TextSendMessage(text=str(body)))

        try:
            e = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in e:
            if isinstance(event, MessageEvent):
                if event.message.text in department_number.keys():
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=department_number[event.message.text]))
                elif event.message.text.strip('系') in department_name.keys():
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=department_name[event.message.text]))
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

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
