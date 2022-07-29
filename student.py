import os
import time

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


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent)
def handle_message(event):
    if isinstance(event, MessageEvent):
        if event.message.text.isdecimal() and event.message.text[0] == '4' and 8 <= len(event.message.text) <= 9:
            url = 'https://lms.ntpu.edu.tw/' + event.message.text
            header = {'user-agent': UserAgent().random}
            web = requests.get(url, headers=header)
            web.encoding = 'utf-8'

            html = BS4(web.text, 'html.parser')
            name = html.find('div', {'class': 'infoPath'})

            if name is None:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='學號' + event.message.text + '不存在'))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=name.find('a').text))

        elif event.message.text.strip('系') in department_number.keys():
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=department_number[event.message.text.strip('系')]))

        elif event.message.text in department_name.keys():
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=department_name[event.message.text] + '系'))

        elif event.message.text.isdecimal() and 2 <= len(event.message.text) <= 4:
            year = int(event.message.text) if int(event.message.text) < 1911 else int(event.message.text) - 1911

            if year > time.localtime(time.time()).tm_year:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你未來人??'))
            elif year < 90:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='學校都還沒蓋好，急什麼XD'))
            elif year < 95:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='資料未建檔'))
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='選擇模式',
                        template=ConfirmTemplate(
                            thumbnail_image_url='https://new.ntpu.edu.tw/assets/logo/ntpu_logo.png',
                            title='是否要查詢 ' + str(year) + ' 學年度的學生',
                            actions=[
                                PostbackAction(
                                    label='哪次不是',
                                    text='開始查詢',
                                    data='查詢全系' + str(year)
                                ),
                                MessageAction(
                                    label='我在想想',
                                    text='再啦ㄍಠ_ಠ'
                                )
                            ]
                        )
                    )
                )
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='學號 -> 姓名\n系名 -> 系代號\n系代號 -> 系名\n年分 -> 全系'))

    elif isinstance(event, PostbackEvent):
        if event.postback.data.startswith('查詢全系'):
            line_bot_api.reply_message(
                event.reply_token,
                TemplateSendMessage(
                    alt_text='選擇學院群',
                    template=ButtonsTemplate(
                        # thumbnail_image_url='https://new.ntpu.edu.tw/assets/logo/ntpu_logo.png',
                        title='選擇學院群',
                        text='請選擇科系所屬學院群',
                        actions=[
                            PostbackAction(
                                label='文法商',
                                text='文法商',
                                data='文法商' + event.postback.data.split('查詢全系')[1]
                            ),
                            PostbackAction(
                                label='公社電資',
                                text='公社電資',
                                data='公社電資' + event.postback.data.split('查詢全系')[1]
                            )
                        ]
                    )
                )
            )

        elif event.postback.startswith('文法商'):
            line_bot_api.reply_message(
                event.reply_token,
                TemplateSendMessage(
                    alt_text='選擇學院',
                    template=ButtonsTemplate(
                        # thumbnail_image_url='https://new.ntpu.edu.tw/assets/logo/ntpu_logo.png',
                        title='選擇學院',
                        text='請選擇科系所屬學院',
                        actions=[
                            PostbackAction(
                                label='人文學院',
                                text='人文學院',
                                data='人文學院' + event.postback.data.split('文法商')[1]
                            ),
                            PostbackAction(
                                label='法律學院',
                                text='法律學院',
                                data='法律學院' + event.postback.data.split('文法商')[1]
                            ),
                            PostbackAction(
                                label='商學院',
                                text='商學院',
                                data='商學院' + event.postback.data.split('文法商')[1]
                            )
                        ]
                    )
                )
            )

        elif event.postback.data.startswith('公社電資'):
            line_bot_api.reply_message(
                event.reply_token,
                TemplateSendMessage(
                    alt_text='選擇學院',
                    template=ButtonsTemplate(
                        # thumbnail_image_url='https://new.ntpu.edu.tw/assets/logo/ntpu_logo.png',
                        title='選擇學院',
                        text='請選擇科系所屬學院',
                        actions=[
                            PostbackAction(
                                label='公共事務學院',
                                text='公共事務學院',
                                data='公共事務學院' + event.postback.data.split('公社電資')[1]
                            ),
                            PostbackAction(
                                label='社會科學學院',
                                text='社會科學學院',
                                data='社會科學學院' + event.postback.data.split('公社電資')[1]
                            ),
                            PostbackAction(
                                label='電機資訊學院',
                                text='電機資訊學院',
                                data='電機資訊學院' + event.postback.data.split('公社電資')[1]
                            )
                        ]
                    )
                )
            )

        elif event.postback.data.startswith('人文學院'):
            line_bot_api.reply_message(
                event.reply_token,
                TemplateSendMessage(
                    alt_text='選擇科系',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https://walkinto.in/upload/-192z7YDP8-JlchfXtDvI.JPG',
                        title='選擇科系',
                        text='請選擇科系',
                        actions=[
                            PostbackAction(
                                label='中國文學系',
                                text='中國文學系',
                                data=event.postback.data.split('人文學院')[1] + ' ' + department_number['中文']
                            ),
                            PostbackAction(
                                label='應用外語學系',
                                text='應用外語學系',
                                data=event.postback.data.split('人文學院')[1] + ' ' + department_number['應外']
                            ),
                            PostbackAction(
                                label='歷史學系',
                                text='歷史學系',
                                data=event.postback.data.split('人文學院')[1] + ' ' + department_number['歷史']
                            )
                        ]
                    )
                )
            )

        elif event.postback.data.startswith('法律學院'):
            line_bot_api.reply_message(
                event.reply_token,
                TemplateSendMessage(
                    alt_text='選擇組別',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https://walkinto.in/upload/byupdk9PvIZyxupOy9Dw8.JPG',
                        title='選擇組別',
                        text='請選擇組別',
                        actions=[
                            PostbackAction(
                                label='法學組',
                                text='法學組',
                                data=event.postback.data.split('法律學院')[1] + ' ' + department_number['法學']
                            ),
                            PostbackAction(
                                label='司法組',
                                text='司法組',
                                data=event.postback.data.split('法律學院')[1] + ' ' + department_number['司法']
                            ),
                            PostbackAction(
                                label='財法祖',
                                text='財法祖',
                                data=event.postback.data.split('法律學院')[1] + ' ' + department_number['財法']
                            )
                        ]
                    )
                )
            )

        elif event.postback.data.startswith('商學院'):
            line_bot_api.reply_message(
                event.reply_token,
                TemplateSendMessage(
                    alt_text='選擇科系',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https://walkinto.in/upload/ZJum7EYwPUZkedmXNtvPL.JPG',
                        title='選擇科系',
                        text='請選擇科系',
                        actions=[
                            PostbackAction(
                                label='企業管理學系',
                                text='企業管理學系',
                                data=event.postback.data.split('商學院')[1] + ' ' + department_number['企管']
                            ),
                            PostbackAction(
                                label='金融與合作經濟學系',
                                text='金融與合作經濟學系',
                                data=event.postback.data.split('商學院')[1] + ' ' + department_number['金融']
                            ),
                            PostbackAction(
                                label='會計學系',
                                text='會計學系',
                                data=event.postback.data.split('商學院')[1] + ' ' + department_number['會計']
                            ),
                            PostbackAction(
                                label='統計學系',
                                text='統計學系',
                                data=event.postback.data.split('商學院')[1] + ' ' + department_number['統計']
                            )
                        ]
                    )
                )
            )

        elif event.postback.data.startswith('公共事務學院'):
            line_bot_api.reply_message(
                event.reply_token,
                TemplateSendMessage(
                    alt_text='選擇科系',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https://walkinto.in/upload/ZJhs4wEaDIWklhiVwV6DI.jpg',
                        title='選擇科系',
                        text='請選擇科系',
                        actions=[
                            PostbackAction(
                                label='公共行政暨政策學系',
                                text='公共行政暨政策學系',
                                data=event.postback.data.split('公共事務學院')[1] + ' ' + department_number['公行']
                            ),
                            PostbackAction(
                                label='不動產與城鄉環境學系',
                                text='不動產與城鄉環境學系',
                                data=event.postback.data.split('公共事務學院')[1] + ' ' + department_number['不動']
                            ),
                            PostbackAction(
                                label='財政學系',
                                text='財政學系',
                                data=event.postback.data.split('公共事務學院')[1] + ' ' + department_number['財政']
                            )
                        ]
                    )
                )
            )

        elif event.postback.data.startswith('社會科學學院'):
            line_bot_api.reply_message(
                event.reply_token,
                TemplateSendMessage(
                    alt_text='選擇科系',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https://walkinto.in/upload/WyPbshN6DIZ1gvZo2NTvU.JPG',
                        title='選擇科系',
                        text='請選擇科系',
                        actions=[
                            PostbackAction(
                                label='經濟學系',
                                text='經濟學系',
                                data=event.postback.data.split('社會科學學院')[1] + ' ' + department_number['經濟']
                            ),
                            PostbackAction(
                                label='社會學系',
                                text='社會學系',
                                data=event.postback.data.split('社會科學學院')[1] + ' ' + department_number['社學']
                            ),
                            PostbackAction(
                                label='社會工作學系',
                                text='社會工作學系',
                                data=event.postback.data.split('社會科學學院')[1] + ' ' + department_number['社工']
                            )
                        ]
                    )
                )
            )

        elif event.postback.data.startswith('電機資訊學院'):
            line_bot_api.reply_message(
                event.reply_token,
                TemplateSendMessage(
                    alt_text='選擇科系',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https://walkinto.in/upload/bJ9zWWHaPLWJg9fW-STD8.png',
                        title='選擇科系',
                        text='請選擇科系',
                        actions=[
                            PostbackAction(
                                label='電機工程學系',
                                text='電機工程學系',
                                data=event.postback.data.split('電機資訊學院')[1] + ' ' + department_number['電機']
                            ),
                            PostbackAction(
                                label='資訊工程學系',
                                text='資訊工程學系',
                                data=event.postback.data.split('電機資訊學院')[1] + ' ' + department_number['資工']
                            ),
                            PostbackAction(
                                label='通訊工程學系',
                                text='通訊工程學系',
                                data=event.postback.data.split('電機資訊學院')[1] + ' ' + department_number['通訊']
                            )
                        ]
                    )
                )
            )

        else:
            url = 'http://lms.ntpu.edu.tw/portfolio/search.php?fmScope=2&page=1&fmKeyword=' + "".join(event.postback.data.split(' '))
            header = {'user-agent': UserAgent().random}
            web = requests.get(url, headers=header)
            web.encoding = 'utf-8'

            html = BS4(web.text, 'html.parser')
            pages = len(html.find_all('span', {'class': 'item'})) - 1

            reply_message = ""
            people_cnt = 0
            for i in range(1, pages + 1):
                # time.sleep(1)

                url = 'http://lms.ntpu.edu.tw/portfolio/search.php?fmScope=2&page=' + str(i) + '&fmKeyword=' + "".join(event.postback.data.split(' '))
                header = {'user-agent': UserAgent().random}
                web = requests.get(url, headers=header)
                web.encoding = 'utf-8'

                html = BS4(web.text, 'html.parser')
                for item in html.find_all('div', {'class': 'bloglistTitle'}):
                    name = item.find('a').text
                    number = item.find('a').get('href').split('/')[-1]
                    reply_message += name + ' ' + number + '\n'
                    people_cnt += 1

            reply_message += '\n' + event.postback.data.split(' ')[0] + '學年度' + department_name[event.postback.data.split(' ')[1]]\
                             + '系總共有' + str(people_cnt) + '位學生'

            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
