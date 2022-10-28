import sys
import settings

from linebot import LineBotApi
from linebot.models import *

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

line_bot_api.push_message(
    settings.user_id,
    TextSendMessage(
        text='%s級地震將於%s秒內抵達' % (sys.argv[1], sys.argv[2]),
        sender=Sender(name='安妮亞', icon_url='https://spy-family.net/assets/img/special/episode9/04.png')
    )
)
