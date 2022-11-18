# -*- coding:utf-8 -*-
import os
import random
import string
import time
from typing import Dict

import requests
from bs4 import BeautifulSoup as Bs4
from flask import Flask, request, abort, redirect
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = Flask(__name__)

department_number = {
    '法律': '71', '法學': '712', '司法': '714', '財法': '716',
    '公行': '72',
    '經濟': '73',
    '社學': '742', '社工': '744',
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

full_department_number = {
    '法律學系': '71', '法學組': '712', '司法組': '714', '財經法組': '716',
    '公共行政暨政策學系': '72',
    '經濟學系': '73',
    '社會學系': '742', '社會工作學系': '744',
    '財政學系': '75',
    '不動產與城鄉環境學系': '76',
    '會計學系': '77',
    '統計學系': '78',
    '企業管理學系': '79',
    '金融與合作經營學系': '80',
    '中國文學系': '81',
    '應用外語學系': '82',
    '歷史學系': '83',
    '休閒運動管理學系': '84',
    '資訊工程學系': '85',
    '通訊工程學系': '86',
    '電機工程學系': '87'
}

all_department_number = ['712', '714', '716', '72', '73', '742', '744', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87']

department_name = {v: k for k, v in department_number.items()}
full_department_name = {v: k for k, v in full_department_number.items()}
student_name: Dict[str, str]
start = True

sticker = {
    '安妮亞': [
        'https://spy-family.net/assets/img/special/08.png',
        'https://spy-family.net/assets/img/special/11.png',
        'https://spy-family.net/assets/img/special/02.png',
        'https://spy-family.net/assets/img/special/05.png',
        'https://spy-family.net/assets/img/special/anya/01.png',
        'https://spy-family.net/assets/img/special/anya/02.png',
        'https://spy-family.net/assets/img/special/anya/05.png',
        'https://spy-family.net/assets/img/special/anya/07.png',
        'https://spy-family.net/assets/img/special/anya/08.png',
        'https://spy-family.net/assets/img/special/anya/10.png',
        'https://spy-family.net/assets/img/special/anya/11.png',
        'https://spy-family.net/assets/img/special/anya/14.png',
        'https://spy-family.net/assets/img/special/anya/15.png',
        'https://spy-family.net/assets/img/special/anya/17.png',
        'https://spy-family.net/assets/img/special/anya/18.png',
        'https://spy-family.net/assets/img/special/anya/20.png',
        'https://spy-family.net/assets/img/special/anya/21.png',
        'https://spy-family.net/assets/img/special/anya/22.png',
        'https://spy-family.net/assets/img/special/anya/23.png',
        'https://spy-family.net/assets/img/special/anya/24.png',
        'https://spy-family.net/assets/img/special/anya/28.png',
        'https://spy-family.net/assets/img/special/anya/30.png',
        'https://spy-family.net/assets/img/special/anya/31.png',
        'https://spy-family.net/assets/img/special/anya/32.png',
        'https://spy-family.net/assets/img/special/anya/35.png',
        'https://spy-family.net/assets/img/special/anya/36.png',
        'https://spy-family.net/assets/img/special/anya/37.png',
        'https://spy-family.net/assets/img/special/episode3/04.png',
        'https://spy-family.net/assets/img/special/episode5/01.png',
        'https://spy-family.net/assets/img/special/episode5/02.png',
        'https://spy-family.net/assets/img/special/episode10/02.png',
        'https://spy-family.net/assets/img/special/episode10/03.png',
        'https://spy-family.net/assets/img/special/episode11/02.png',
        'https://spy-family.net/assets/img/special/episode11/04.png',
        'https://spy-family.net/assets/img/special/episode12/03.png',
        'https://spy-family.net/assets/img/special/episode12/06.png',
    ],
    '安妮亞哭': [
        'https://spy-family.net/assets/img/special/anya/04.png',
        'https://spy-family.net/assets/img/special/anya/06.png',
        'https://spy-family.net/assets/img/special/anya/09.png',
        'https://spy-family.net/assets/img/special/anya/16.png',
        'https://spy-family.net/assets/img/special/anya/19.png',
        'https://spy-family.net/assets/img/special/anya/25.png',
        'https://spy-family.net/assets/img/special/anya/26.png',
        'https://spy-family.net/assets/img/special/anya/27.png',
        'https://spy-family.net/assets/img/special/anya/29.png',
        'https://spy-family.net/assets/img/special/anya/33.png',
        'https://spy-family.net/assets/img/special/anya/38.png',
        'https://spy-family.net/assets/img/special/anya/39.png',
        'https://spy-family.net/assets/img/special/episode4/02.png',
        'https://spy-family.net/assets/img/special/episode7/01.png',
        'https://spy-family.net/assets/img/special/episode9/04.png',
        'https://spy-family.net/assets/img/special/episode11/01.png',
        'https://spy-family.net/assets/img/special/episode11/06.png'
    ],
    '洛伊德': [
        'https://spy-family.net/assets/img/special/07.png',
        'https://spy-family.net/assets/img/special/10.png',
        'https://spy-family.net/assets/img/special/01.png',
        'https://spy-family.net/assets/img/special/04.png',
        'https://spy-family.net/assets/img/special/loid/03.png',
        'https://spy-family.net/assets/img/special/loid/07.png',
        'https://spy-family.net/assets/img/special/loid/08.png',
        'https://spy-family.net/assets/img/special/loid/10.png',
        'https://spy-family.net/assets/img/special/loid/11.png',
        'https://spy-family.net/assets/img/special/loid/15.png',
        'https://spy-family.net/assets/img/special/loid/17.png',
        'https://spy-family.net/assets/img/special/loid/18.png',
        'https://spy-family.net/assets/img/special/loid/20.png',
        'https://spy-family.net/assets/img/special/episode1/01.png',
        'https://spy-family.net/assets/img/special/episode1/05.png',
        'https://spy-family.net/assets/img/special/episode2/06.png',
        'https://spy-family.net/assets/img/special/episode3/01.png',
        'https://spy-family.net/assets/img/special/episode5/04.png',
        'https://spy-family.net/assets/img/special/episode8/05.png',
        'https://spy-family.net/assets/img/special/episode9/03.png',
        'https://spy-family.net/assets/img/special/episode11/05.png'
    ],
    '其他': [
        'https://spy-family.net/assets/img/special/09.png',
        'https://spy-family.net/assets/img/special/12.png',
        'https://spy-family.net/assets/img/special/03.png',
        'https://spy-family.net/assets/img/special/06.png',
        'https://spy-family.net/assets/img/special/yor/01.png',
        'https://spy-family.net/assets/img/special/yor/03.png',
        'https://spy-family.net/assets/img/special/yor/11.png',
        'https://spy-family.net/assets/img/special/yor/15.png',
        'https://spy-family.net/assets/img/special/yor/17.png',
        'https://spy-family.net/assets/img/special/episode1/03.png',
        'https://spy-family.net/assets/img/special/episode2/06.png',
        'https://spy-family.net/assets/img/special/episode3/03.png',
        'https://spy-family.net/assets/img/special/episode3/05.png',
        'https://spy-family.net/assets/img/special/episode4/04.png',
        'https://spy-family.net/assets/img/special/episode4/05.png',
        'https://spy-family.net/assets/img/special/episode4/06.png',
        'https://spy-family.net/assets/img/special/episode6/02.png',
        'https://spy-family.net/assets/img/special/episode6/03.png',
        'https://spy-family.net/assets/img/special/episode6/04.png',
        'https://spy-family.net/assets/img/special/episode6/05.png',
        'https://spy-family.net/assets/img/special/episode6/06.png',
        'https://spy-family.net/assets/img/special/episode7/02.png',
        'https://spy-family.net/assets/img/special/episode7/03.png',
        'https://spy-family.net/assets/img/special/episode7/04.png',
        'https://spy-family.net/assets/img/special/episode7/06.png',
        'https://spy-family.net/assets/img/special/episode8/01.png',
        'https://spy-family.net/assets/img/special/episode9/01.png',
        'https://spy-family.net/assets/img/special/episode10/04.png',
        'https://spy-family.net/assets/img/special/episode10/05.png',
        'https://spy-family.net/assets/img/special/episode10/06.png',
        'https://spy-family.net/assets/img/special/episode12/05.png',
        'https://spy-family.net/assets/img/special/summermission01/01.png',
        'https://spy-family.net/assets/img/special/summermission01/04.png',
    ]
}

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


@app.route('/')
def github():
    return redirect('https://github.com/garyellow/ntpu-student-id-linebot')


@app.route('/renew')
def renew():
    global student_name
    cur_year = time.localtime(time.time()).tm_year - 1911
    new_student_name: Dict[str, str] = {}

    for year in range(cur_year - 5, cur_year):
        with requests.Session() as s:
            s.keep_alive = False

            for dep in all_department_number:
                time.sleep(random.uniform(0.01, 0.05))
                url = 'http://120.126.197.52/portfolio/search.php?fmScope=2&page=1&fmKeyword=4' + str(year) + dep
                web = s.get(url)
                web.encoding = 'utf-8'

                html = Bs4(web.text, 'html.parser')
                pages = len(html.find_all('span', {'class': 'item'}))

                for item in html.find_all('div', {'class': 'bloglistTitle'}):
                    name = item.find('a').text
                    number = item.find('a').get('href').split('/')[-1]
                    new_student_name[number] = name

                for i in range(2, pages):
                    time.sleep(random.uniform(0.01, 0.05))

                    url = 'http://120.126.197.52/portfolio/search.php?fmScope=2&page=' + str(i) + '&fmKeyword=4' + str(year) + dep
                    web = s.get(url)
                    web.encoding = 'utf-8'

                    html = Bs4(web.text, 'html.parser')
                    for item in html.find_all('div', {'class': 'bloglistTitle'}):
                        name = item.find('a').text
                        number = item.find('a').get('href').split('/')[-1]
                        new_student_name[number] = name

    student_name = new_student_name.copy()
    return 'OK'


@app.route('/check')
def healthy():
    global start
    if start:
        start = False
        renew()

    return 'OK'


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    # print('Request body: ' + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent)
def handle_message(event):
    global student_name
    if event.message.type in ['image', 'video', 'audio', 'file']:
        return

    if event.message.type != 'text':
        img = random.choice(random.choice(list(sticker.values())))
        line_bot_api.reply_message(
            event.reply_token, ImageSendMessage(
                original_content_url=img,
                preview_image_url=img,
                sender=Sender(icon_url=random.choice(random.choice(list(sticker.values()))))
            )
        )
        return

    text = ''.join(x for x in event.message.text if x not in string.whitespace + string.punctuation)
    if text.isdecimal():
        if text in full_department_name.keys():
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=full_department_name[text],
                    sender=Sender(name='安妮亞', icon_url=random.choice(sticker['安妮亞']))
                )
            )

        elif text[0] == '4' and 8 <= len(text) <= 9:
            name = ""
            if not student_name.__contains__(text):
                url = 'http://120.126.197.52/portfolio/search.php?fmScope=2&page=1&fmKeyword=' + text
                web = requests.get(url)
                web.encoding = 'utf-8'

                html = Bs4(web.text, 'html.parser')
                person = html.find('div', {'class': 'bloglistTitle'})

                if person is None:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(
                            text='學號' + text + '不存在OAO',
                            sender=Sender(name='安妮亞', icon_url=random.choice(sticker['安妮亞哭']))
                        )
                    )
                else:
                    name += person.find('a').text
            else:
                name += student_name[text]

            over_hun = len(text) == 9

            year = text[1:over_hun + 3]
            department = text[over_hun + 3:over_hun + 5]

            if department in [department_number['法律'], department_number['社學'][0:2]]:
                department += text[over_hun + 5]

            message = year + '學年度 '

            if department[0:2] == '71':
                message += '法律系 ' + department_name[department] + '組 '
            elif department[0:2] == '74':
                message += department_name[department] + '系 '
            else:
                message += department_name[department] + '系 '

            message += name

            if department[0:2] == department_number['法律']:
                show_text = '搜尋' + year + '學年度法律系' + department_name[department] + '組'
            else:
                show_text = '搜尋' + year + '學年度' + department_name[department] + '系'

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=message,
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=PostbackAction(
                                    label=show_text,
                                    display_text='正在' + show_text,
                                    data=year + ' ' + department,
                                    input_option='closeRichMenu'
                                )
                            )
                        ]
                    ),
                    sender=Sender(name='洛伊德', icon_url=random.choice(sticker['洛伊德']))
                )
            )

        elif 2 <= len(text) <= 4:
            year = int(text) if int(text) < 1911 else int(text) - 1911

            if year > time.localtime(time.time()).tm_year - 1911:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='你未來人？(⊙ˍ⊙)', sender=Sender(name='安妮亞', icon_url=random.choice(sticker['安妮亞'])))
                )
            elif year < 90:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='學校都還沒蓋好(￣▽￣)', sender=Sender(name='安妮亞', icon_url=random.choice(sticker['安妮亞'])))
                )
            elif year < 95:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='資料未建檔', sender=Sender(name='安妮亞', icon_url=random.choice(sticker['安妮亞'])))
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='確認學年度',
                        template=ConfirmTemplate(
                            text='是否要搜尋 ' + str(year) + ' 學年度的學生',
                            actions=[
                                PostbackAction(
                                    label='哪次不是',
                                    display_text='哪次不是',
                                    data='搜尋全系' + str(year),
                                    input_option='openRichMenu'
                                ),
                                PostbackAction(
                                    label='我在想想',
                                    display_text='再啦ㄍಠ_ಠ',
                                    data='兇',
                                    input_option='openKeyboard'
                                )
                            ]
                        ),
                        sender=Sender(icon_url=random.choice(sticker['其他']))
                    )
                )

    elif text == '所有系代碼':
        message = '\n'.join([x[0] + '系 -> ' + x[1] for x in department_number.items()])
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=message,
            sender=Sender(name='安妮亞', icon_url=random.choice(sticker['安妮亞']))))

    elif text.strip('系') in department_number.keys():
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=department_number[text.strip('系')],
                quick_reply=QuickReply(items=[QuickReplyButton(action=MessageAction(label='所有系代碼', text='所有系代碼'))]),
                sender=Sender(name='安妮亞', icon_url=random.choice(sticker['安妮亞']))
            )
        )

    elif text in full_department_number.keys():
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=full_department_number[text],
                quick_reply=QuickReply(items=[QuickReplyButton(action=MessageAction(label='所有系代碼', text='所有系代碼'))]),
                sender=Sender(name='安妮亞', icon_url=random.choice(sticker['安妮亞']))
            )
        )

    elif text in student_name.values():
        message = ""
        for key, value in student_name.items():
            if value == text:
                if message != "":
                    message += "\n"

                over_hun = len(key) == 9

                year = key[1:over_hun + 3]
                department = key[over_hun + 3:over_hun + 5]

                if department in [department_number['法律'], department_number['社學'][0:2]]:
                    department += key[over_hun + 5]

                message += year + '學年度 '

                if department[0:2] == '71':
                    message += '法律系 ' + department_name[department] + '組 '
                elif department[0:2] == '74':
                    message += department_name[department] + '系 '
                else:
                    message += department_name[department] + '系 '

                message += key

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=message,
                sender=Sender(name='洛伊德', icon_url=random.choice(sticker['洛伊德']))
            )
        )


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == '使用說明':
        mes_sender = Sender(name='安妮亞', icon_url=random.choice(sticker['安妮亞']))
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='輸入學號可獲取學生姓名\n輸入系名可獲取系代碼\n輸入系代碼可獲取系名\n輸入入學學年獲取某系的學生名單',
                                sender=mes_sender),
                TextSendMessage(text='輸入範例\n學號：412345678\n系名：資工系、資訊工程學系\n系代碼：85\n' +
                                     '入學學年：' + str(time.localtime(time.time()).tm_year - 1911) + '、' + str(time.localtime(time.time()).tm_year),
                                sender=mes_sender),
            ]
        )

    elif event.postback.data == '兇':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='泥好兇喔~~இ௰இ', sender=Sender(name='安妮亞', icon_url=random.choice(sticker['安妮亞哭'])))
        )

    elif event.postback.data.startswith('搜尋全系'):
        year = event.postback.data.split('搜尋全系')[1]

        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text='選擇學院群',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://new.ntpu.edu.tw/assets/logo/ntpu_logo.png',
                    title='選擇學院群',
                    text='請選擇科系所屬學院群',
                    actions=[
                        PostbackAction(
                            label='文法商',
                            display_text='文法商',
                            data='文法商' + year
                        ),
                        PostbackAction(
                            label='公社電資',
                            display_text='公社電資',
                            data='公社電資' + year
                        )
                    ]
                ),
                sender=Sender(icon_url=random.choice(sticker['其他']))
            )
        )

    elif event.postback.data.startswith('文法商'):
        year = event.postback.data.split('文法商')[1]

        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text='選擇學院',
                template=ButtonsTemplate(
                    title='選擇學院',
                    text='請選擇科系所屬學院',
                    actions=[
                        PostbackAction(
                            label='人文學院',
                            display_text='人文學院',
                            data='人文學院' + year
                        ),
                        PostbackAction(
                            label='法律學院',
                            display_text='法律學院',
                            data='法律學院' + year
                        ),
                        PostbackAction(
                            label='商學院',
                            display_text='商學院',
                            data='商學院' + year
                        )
                    ]
                ),
                sender=Sender(icon_url=random.choice(sticker['其他']))
            )
        )

    elif event.postback.data.startswith('公社電資'):
        year = event.postback.data.split('公社電資')[1]

        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text='選擇學院',
                template=ButtonsTemplate(
                    title='選擇學院',
                    text='請選擇科系所屬學院',
                    actions=[
                        PostbackAction(
                            label='公共事務學院',
                            display_text='公共事務學院',
                            data='公共事務學院' + year
                        ),
                        PostbackAction(
                            label='社會科學學院',
                            display_text='社會科學學院',
                            data='社會科學學院' + year
                        ),
                        PostbackAction(
                            label='電機資訊學院',
                            display_text='電機資訊學院',
                            data='電機資訊學院' + year
                        )
                    ]
                ),
                sender=Sender(icon_url=random.choice(sticker['其他']))
            )
        )

    elif event.postback.data.startswith('人文學院'):
        year = event.postback.data.split('人文學院')[1]

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
                            display_text='正在搜尋' + year + '學年度中文系',
                            data=year + ' ' + department_number['中文'],
                            input_option='closeRichMenu'
                        ),
                        PostbackAction(
                            label='應用外語學系',
                            display_text='正在搜尋' + year + '學年度應外系',
                            data=year + ' ' + department_number['應外'],
                            input_option='closeRichMenu'
                        ),
                        PostbackAction(
                            label='歷史學系',
                            display_text='正在搜尋' + year + '學年度歷史系',
                            data=year + ' ' + department_number['歷史'],
                            input_option='closeRichMenu'
                        )
                    ]
                ),
                sender=Sender(icon_url=random.choice(sticker['其他']))
            )
        )

    elif event.postback.data.startswith('法律學院'):
        year = event.postback.data.split('法律學院')[1]

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
                            display_text='正在搜尋' + year + '學年度法律系法學組',
                            data=year + ' ' + department_number['法學'],
                            input_option='closeRichMenu'
                        ),
                        PostbackAction(
                            label='司法組',
                            display_text='正在搜尋' + year + '學年度法律系司法組',
                            data=year + ' ' + department_number['司法'],
                            input_option='closeRichMenu'
                        ),
                        PostbackAction(
                            label='財經法組',
                            display_text='正在搜尋' + year + '學年度法律系財法組',
                            data=year + ' ' + department_number['財法'],
                            input_option='closeRichMenu'
                        )
                    ]
                ),
                sender=Sender(icon_url=random.choice(sticker['其他']))
            )
        )

    elif event.postback.data.startswith('商學院'):
        year = event.postback.data.split('商學院')[1]

        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text='選擇科系',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://walkinto.in/upload/ZJum7EYwPUZkedmXNtvPL.JPG',
                    title='選擇科系',
                    text='請選擇科系 (休運系請直接點圖片)',
                    default_action=PostbackAction(
                        label='休閒運動管理學系',
                        display_text='正在搜尋' + year + '學年度休運系',
                        data=year + ' ' + department_number['休運'],
                        input_option='closeRichMenu'
                    ),
                    actions=[
                        PostbackAction(
                            label='企業管理學系',
                            display_text='正在搜尋' + year + '學年度企管系',
                            data=year + ' ' + department_number['企管'],
                            input_option='closeRichMenu'
                        ),
                        PostbackAction(
                            label='金融與合作經營學系',
                            display_text='正在搜尋' + year + '學年度金融系',
                            data=year + ' ' + department_number['金融'],
                            input_option='closeRichMenu'
                        ),
                        PostbackAction(
                            label='會計學系',
                            display_text='正在搜尋' + year + '學年度會計系',
                            data=year + ' ' + department_number['會計'],
                            input_option='closeRichMenu'
                        ),
                        PostbackAction(
                            label='統計學系',
                            display_text='正在搜尋' + year + '學年度統計系',
                            data=year + ' ' + department_number['統計'],
                            input_option='closeRichMenu'
                        )
                    ]
                ),
                sender=Sender(icon_url=random.choice(sticker['其他']))
            )
        )

    elif event.postback.data.startswith('公共事務學院'):
        year = event.postback.data.split('公共事務學院')[1]

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
                            display_text='正在搜尋' + year + '學年度公行系',
                            data=year + ' ' + department_number['公行'],
                            input_option='closeRichMenu'
                        ),
                        PostbackAction(
                            label='不動產與城鄉環境學系',
                            display_text='正在搜尋' + year + '學年度不動系',
                            data=year + ' ' + department_number['不動'],
                            input_option='closeRichMenu'
                        ),
                        PostbackAction(
                            label='財政學系',
                            display_text='正在搜尋' + year + '學年度財政系',
                            data=year + ' ' + department_number['財政'],
                            input_option='closeRichMenu'
                        )
                    ]
                ),
                sender=Sender(icon_url=random.choice(sticker['其他']))
            )
        )

    elif event.postback.data.startswith('社會科學學院'):
        year = event.postback.data.split('社會科學學院')[1]

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
                            display_text='正在搜尋' + year + '學年度經濟系',
                            data=year + ' ' + department_number['經濟'],
                            input_option='closeRichMenu'
                        ),
                        PostbackAction(
                            label='社會學系',
                            display_text='正在搜尋' + year + '學年度社學系',
                            data=year + ' ' + department_number['社學'],
                            input_option='closeRichMenu'
                        ),
                        PostbackAction(
                            label='社會工作學系',
                            display_text='正在搜尋' + year + '學年度社工系',
                            data=year + ' ' + department_number['社工'],
                            input_option='closeRichMenu'
                        )
                    ]
                ),
                sender=Sender(icon_url=random.choice(sticker['其他']))
            )
        )

    elif event.postback.data.startswith('電機資訊學院'):
        year = event.postback.data.split('電機資訊學院')[1]

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
                            display_text='正在搜尋' + year + '學年度電機系',
                            data=year + ' ' + department_number['電機'],
                            input_option='closeRichMenu'
                        ),
                        PostbackAction(
                            label='資訊工程學系',
                            display_text='正在搜尋' + year + '學年度資工系',
                            data=year + ' ' + department_number['資工'],
                            input_option='closeRichMenu'
                        ),
                        PostbackAction(
                            label='通訊工程學系',
                            display_text='正在搜尋' + year + '學年度通訊系',
                            data=year + ' ' + department_number['通訊'],
                            input_option='closeRichMenu'
                        )
                    ]
                ),
                sender=Sender(icon_url=random.choice(sticker['其他']))
            )
        )

    else:
        yd = ''.join(event.postback.data.split(' '))
        with requests.Session() as s:
            s.keep_alive = False

            url = 'http://120.126.197.52/portfolio/search.php?fmScope=2&page=1&fmKeyword=4' + yd
            web = s.get(url)
            web.encoding = 'utf-8'

            html = Bs4(web.text, 'html.parser')
            pages = len(html.find_all('span', {'class': 'item'}))

            message = ''
            people_cnt = 0

            for item in html.find_all('div', {'class': 'bloglistTitle'}):
                name = item.find('a').text
                number = item.find('a').get('href').split('/')[-1]
                message += name.ljust(10, '.') + number + '\n' if name[0] in string.ascii_letters else name.ljust(6, '．') + number + '\n'
                people_cnt += 1

            for i in range(2, pages):
                time.sleep(random.uniform(0.01, 0.05))

                url = 'http://120.126.197.52/portfolio/search.php?fmScope=2&page=' + str(i) + '&fmKeyword=4' + yd
                web = s.get(url)
                web.encoding = 'utf-8'

                html = Bs4(web.text, 'html.parser')
                for item in html.find_all('div', {'class': 'bloglistTitle'}):
                    name = item.find('a').text
                    number = item.find('a').get('href').split('/')[-1]
                    message += name.ljust(10, '.') + number + '\n' if name[0] in string.ascii_letters else name.ljust(6, '．') + number + '\n'
                    people_cnt += 1

        if event.postback.data.split(' ')[1][0:2] == department_number['法律']:
            message += '\n' + event.postback.data.split(' ')[0] + '學年度法律系' + department_name[event.postback.data.split(' ')[1]] \
                       + '組共有' + str(people_cnt) + '位學生'
        else:
            message += '\n' + event.postback.data.split(' ')[0] + '學年度' + department_name[event.postback.data.split(' ')[1]] \
                       + '系共有' + str(people_cnt) + '位學生'

        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=message, sender=Sender(name='洛伊德', icon_url=random.choice(sticker['洛伊德']))))


@handler.add(FollowEvent)
@handler.add(JoinEvent)
@handler.add(MemberJoinedEvent)
def handle_follow_join(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(
            text='''泥好~~我是學號姓名查詢機器人🤖
可以用學號查詢到學生姓名
要看使用說明可以點選下方選單

有問題可以先去看常見問題
若無法解決或找到Bug
可以再到GitHub提出

資料來源：國立臺北大學數位學苑2.0''',
            sender=Sender(name='安妮亞', icon_url=random.choice(sticker['安妮亞']))
        )
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
