from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from get_jav_girls import *
from return_one_question import *
from database_king import *
from database import find_info, new_restaurant, delete_restaurant, update_menu, find_db
import os
import json
import random
app = Flask(__name__)

line_bot_api = LineBotApi('wX4kW8fAYOMgibY/ZAbvqGvT4ILRNRQMr5jGRERI2BVNi/xeULoN7Sl4c9QIS4zC3Mcz57jb0fnXmkoQGhKF5xqfwLzgGtWhtaqNXEVbT5i7OmHB51u5TBWKn08uXAiTPX46sy7DSrf7uAiq/0uDBgdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token
handler = WebhookHandler('5050d88d69a3ebcea7f4820874ff9e90') #Your Channel Secret

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

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text #message from user
    # user_dict = json.loads(str(event.source))
    userId = json.loads(str(event.source))['userId']
    status = userStatus(userId)
    sexual = userSexual(userId)
    print(text)
    print(sexual)
    # localtime = time.asctime( time.localtime(time.time()) )
    # group_id = str(event.source)[13:46]
    # myCollection.insert_many([{"group_id":group_id,"text":text,"time":localtime}])
    if status == "$start":
      if len(text) <= 10:
        set_userName(userId, text)
        text_message = buttons_template = FlexSendMessage(
            alt_text='開始挑戰',
            contents= BubbleContainer(
                      body = BoxComponent(
                              layout = "vertical",
                              contents = [TextComponent(text = "歡迎!" + text + '準備好挑戰了嗎?', wrap = True)]
                                            ),
                      footer = BoxComponent(
                              layout = "horizontal",
                              contents = [ButtonComponent(style = "primary", action = MessageAction(label = "我要改名", text = "我要改名")),
                                          SeparatorComponent(margin = 'xl'),
                                          ButtonComponent(style = "primary", action = MessageAction(label = "開始挑戰", text = "答題"))]
                                            )
                      )

        )
        line_bot_api.reply_message(
          event.reply_token,
          text_message)
        return 0
      else:
        text_message = TextSendMessage(text= "暱稱太長喔，請重新輸入")
        line_bot_api.reply_message(
          event.reply_token,
          text_message)
        return 0
    elif status.isalpha() and judge_pure_english(text):
      if ord(status) == 65313:
        status = 'A'
      elif ord(status) == 65314:
        status = 'B'
      elif ord(status) == 65315:
        status == 'C'
      if status.upper() == text:
        after_answer(userId, 1)
        if sexual == 0 or sexual == 1:
          hero_component = ImageComponent(
                                url = read_src_kanna_jpg(),
                                size = "full")
        elif sexual == 2:
          hero_component = ImageComponent(
                                url = read_src_ogisome_jpg(),
                                size = "full")
        elif sexual == 3:
          hero_component = ImageComponent(
                                url = read_src_cute_jpg(),
                                size = "full")
        elif sexual == 4:
          hero_component = ImageComponent(
                                url = read_src_takagi_jpg(),
                                size = "full")
        text_message = FlexSendMessage(
            alt_text='恭喜答對!',
            contents= BubbleContainer(
                      header = BoxComponent(
                              layout = "vertical",
                              contents = [TextComponent(text = "恭喜答對，很聰明呢!", wrap = True)]
                                            ),
                      hero = hero_component,
                      footer = BoxComponent(
                              layout = "horizontal",
                              contents = [ButtonComponent(style = "primary", action = MessageAction(label = "目前成績", text = "目前成績")),
                                          SeparatorComponent(margin = 'xl'),
                                          ButtonComponent(style = "primary", action = MessageAction(label = "繼續挑戰", text = "答題"))]
                                            )
                      )

        )
        line_bot_api.reply_message(
          event.reply_token,
          text_message)
        return 0
      else:
        after_answer(userId, 0)
        if sexual == 0 or sexual == 1:
          hero_component = ImageComponent(
                                url = read_src_pola_jpg(),
                                size = "full")
        elif sexual == 2:
          hero_component = ImageComponent(
                                url = read_src_stickers('mutom'),
                                size = "full")
        elif sexual == 3:
          hero_component = ImageComponent(
                                url = read_src_beastears_jpg(),
                                size = "full")
        elif sexual == 4:
          hero_component = ImageComponent(
                                url = read_src_kizuna_jpg(),
                                size = "full")
        text_message = FlexSendMessage(
            alt_text='可惜答錯!',
            contents= BubbleContainer(
                      header = BoxComponent(
                              layout = "vertical",
                              contents = [TextComponent(text = "可惜答錯QQ，再努力吧!\n答案是:" + status, wrap = True)]
                                            ),
                      hero = hero_component,
                      footer = BoxComponent(
                              layout = "horizontal",
                              contents = [ButtonComponent(style = "primary", action = MessageAction(label = "目前成績", text = "目前成績")),
                                          SeparatorComponent(margin = 'xl'),
                                          ButtonComponent(style = "primary", action = MessageAction(label = "繼續挑戰", text = "答題"))]
                                            )
                      )

        )
        line_bot_api.reply_message(
          event.reply_token,
          text_message)
        return 0
    if '母湯' in text:
      img_src = read_src_mutom_jpg()
      line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(original_content_url= img_src,
                          preview_image_url= img_src))
      return 0
    elif "我要改名" == text:
      re_userName(userId)
      text_message = TextSendMessage(text= "請輸入您的新暱稱(限制10字元以內)")
      line_bot_api.reply_message(
          event.reply_token,
          text_message)
      return 0
    elif "我要換圖" == text:
      text_message = FlexSendMessage(
            alt_text='更換圖片',
            contents= BubbleContainer(
                      body = BoxComponent(
                              layout = "vertical",
                              contents = [TextComponent(text = "請問您想更換成什麼類型的圖片?", wrap = True)]
                                            ),
                      footer = BoxComponent(
                              layout = "horizontal",
                              contents = [BoxComponent(
                                          layout = "vertical",
                                          contents = [ButtonComponent(style = "primary", action = MessageAction(label = "正妹", text = "更換圖片-正妹")),
                                                      SeparatorComponent(margin = 'xl'),
                                                      ButtonComponent(style = "primary", action = MessageAction(label = "帥哥", text = "更換圖片-帥哥"))]
                                                        ),
                                          SeparatorComponent(margin = 'xl'),
                                          BoxComponent(
                                          layout = "vertical",
                                          contents = [ButtonComponent(style = "primary", action = MessageAction(label = "可愛動物", text = "更換圖片-可愛動物")),
                                                      SeparatorComponent(margin = 'xl'),
                                                      ButtonComponent(style = "primary", action = MessageAction(label = "二次元", text = "更換圖片-二次元"))]
                                                        )]
                                            )
                      )

        )
      line_bot_api.reply_message(
        event.reply_token,
        text_message)
      return 0
    elif "更換圖片-" == text[:5]:
      if text[5:] == "正妹":
        set_userSexual(userId, 1)
      elif text[5:] == "帥哥":
        set_userSexual(userId, 2)
      elif text[5:] == "可愛動物":
        set_userSexual(userId, 3)
      elif text[5:] == "二次元":
        set_userSexual(userId, 4)
      else:
        return 0
      text_message = TextSendMessage(text= "已成功更換圖片類型")
      line_bot_api.reply_message(
          event.reply_token,
          text_message)
      return 0
    elif "開始挑戰" == text:
      exist_or_not = initSeting(userId)
      if exist_or_not == False:
        text_message = TextSendMessage(text= "歡迎挑戰台大知識王，請輸入您的暱稱(限制10字元以內)")
        line_bot_api.reply_message(
          event.reply_token,
          text_message)
        return 0
      else:
        text_message = TextSendMessage(text= "您已開始進行挑戰囉!")
        line_bot_api.reply_message(
          event.reply_token,
          text_message)
        return 0
    elif "測試" == text:
      question, choice_1, choice_2, choice_3, answer = return_one()
      text_message = TextSendMessage(text="請問" + question + '\n' + '(A)' + choice_1 + '\n' + '(B)' + choice_2 + '\n' + '(C)' + choice_3)
      line_bot_api.reply_message(
        event.reply_token,
        text_message)
      return 0
    elif "答題" == text and status.isalpha():
      text_message = TextSendMessage(text="目前正在答題中，請先答完!")
      line_bot_api.reply_message(
        event.reply_token,
        text_message)
      return 0
    elif "答題" == text and (not status.isalpha()):
        index, index2 = index_index2(userId)
        if index == "wrong":
          text_message = TextSendMessage(text="恭喜你，全部答完囉!")
          line_bot_api.reply_message(
            event.reply_token,
            text_message)
          return 0
        question, choice_1, choice_2, choice_3, answer = return_one(index, index2)
        change_status(userId, answer)
        if sexual == 0 or sexual == 1:
          hero_component = ImageComponent(
                                url = read_src_liyin_jpg(),
                                size = "full")
        elif sexual == 2:
          hero_component = ImageComponent(
                                url = read_src_lee_jpg(),
                                size = "full")
        elif sexual == 3:
          hero_component = ImageComponent(
                                url = read_src_stickers('penguins'),
                                size = "full")
        elif sexual == 4:
          hero_component = ImageComponent(
                                url = read_src_anime_boys_jpg(),
                                size = "full")
        buttons_template = FlexSendMessage(
            alt_text='一個問題',
            contents= BubbleContainer(
                      hero = hero_component,
                      body = BoxComponent(
                              layout = "vertical",
                              contents = [TextComponent(text = "請問" + question, wrap = True),
                                          TextComponent(text = '(A)' + choice_1, wrap = True),
                                          TextComponent(text = '(B)' + choice_2, wrap = True),
                                          TextComponent(text = '(C)' + choice_3, wrap = True),]
                                            ),
                      footer = BoxComponent(
                              layout = "horizontal",
                              contents = [ButtonComponent(style = "primary", action = MessageAction(label = "A", text = "A")),
                                          SeparatorComponent(margin = 'xl'),
                                          ButtonComponent(style = "primary", action = MessageAction(label = "B", text = "B")),
                                          SeparatorComponent(margin = 'xl'),
                                          ButtonComponent(style = "primary", action = MessageAction(label = "C", text = "C"))]
                                            )
                      )

        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    elif "目前成績" == text:
      userPoint, userWrong, userRate = user_point(userId)
      if userPoint == "wrong":
        text_message = TextSendMessage(text= "您尚未進行挑戰")
        line_bot_api.reply_message(
          event.reply_token,
          text_message)
        return 0
      else:
        text_message = FlexSendMessage(
            alt_text='目前成績',
            contents= BubbleContainer(
                      body = BoxComponent(
                              layout = "vertical",
                              contents = [TextComponent(text= "您目前答對" + str(userPoint) + '題\n答錯' + str(userWrong) + '題\n正確率為' + str(userRate/100) + '%', wrap = True)]
                                            ),
                      footer = BoxComponent(
                              layout = "horizontal",
                              contents = [ButtonComponent(style = "primary", action = MessageAction(label = "排行榜", text = "排行榜")),
                                          SeparatorComponent(margin = 'xl'),
                                          ButtonComponent(style = "primary", action = MessageAction(label = "繼續挑戰", text = "答題"))]
                                            )
                      )

        )
        line_bot_api.reply_message(
          event.reply_token,
          text_message)
        return 0
    elif "排行榜" == text:
      text_message = FlexSendMessage(
            alt_text='答題風雲榜',
            contents= BubbleContainer(
                      footer = BoxComponent(
                              layout = "horizontal",
                              contents = [ButtonComponent(style = "primary", action = MessageAction(label = "答題風雲榜", text = "答題風雲榜")),
                                          SeparatorComponent(margin = 'xl'),
                                          ButtonComponent(style = "primary", action = MessageAction(label = "正確率風雲榜", text = "正確率風雲榜"))]
                                            )
                      )

        )
      line_bot_api.reply_message(
      event.reply_token,
      text_message)
      return 0
    elif "答題風雲榜" == text:
      max_list, max_list_point = find_max_point()
      userPoint, userWrong, userRate = user_point(userId)
      userName = user_name(userId)
      if userPoint == "wrong":
        return 0

      userPosition = max_list_point.index(userPoint)
      if len(max_list) > 10:
        max_list = max_list[:10]
        max_list_point = max_list_point[:10]

      body_contents = []
      for i in range(len(max_list)):
        text_one = TextComponent(text = str(i+1) + '.' + str(max_list[i]) + " 答對題數:" + str(max_list_point[i]), wrap = True)
        body_contents.append(text_one)
      text_user = TextComponent(text = '\n' + '您的成績:\n' + str(userPosition+1) + '.' + userName + " 答對題數:" + str(userPoint), wrap = True)
      body_contents.append(text_user)
      if sexual == 0 or sexual == 1:
          hero_component = ImageComponent(
                                url = read_src_gaki_jpg(),
                                size = "full")
      elif sexual == 2:
        hero_component = ImageComponent(
                              url = read_src_fengden_jpg(),
                              size = "full")
      elif sexual == 3:
        hero_component = ImageComponent(
                              url = read_src_cats_jpg(),
                              size = "full")
      elif sexual == 4:
        hero_component = ImageComponent(
                              url = read_src_anime_jpg(),
                              size = "full")
      text_message = FlexSendMessage(
            alt_text='答題風雲榜',
            contents= BubbleContainer(
                      header = BoxComponent(
                              layout = "vertical",
                              contents = [TextComponent(text = "答題風雲榜", size = "3xl", align = "center", wrap = True)]
                                            ),
                      hero = hero_component,
                      body = BoxComponent(
                              layout = "vertical",
                              contents = body_contents
                                            ),
                      footer = BoxComponent(
                              layout = "horizontal",
                              contents = [ButtonComponent(style = "primary", action = MessageAction(label = "繼續挑戰", text = "答題"))]
                                            )
                      )

        )
      line_bot_api.reply_message(
      event.reply_token,
      text_message)
      return 0
    elif "正確率風雲榜" == text:
      max_list, max_list_rate = find_max_rate()
      userPoint, userWrong, userRate = user_point(userId)
      userName = user_name(userId)
      if userRate == 0:
        return 0
      if userPoint >= 30:
        userPosition = max_list_rate.index(userRate)
      else:
        userPosition = "None"

      if len(max_list) > 10:
        max_list = max_list[:10]
        max_list_rate = max_list_rate[:10]

      body_contents = []
      for i in range(len(max_list)):
        text_one = TextComponent(text = str(i+1) + '.' + str(max_list[i]) + " 正確率:" + str(max_list_rate[i]/100) + '%', wrap = True)
        body_contents.append(text_one)
      if userPosition != "None":
        text_user = TextComponent(text = '\n' + '您的成績:\n' + str(userPosition+1) + '.' + userName + " 正確率:" + str(userRate/100) + '%', wrap = True)
      else:
        text_user = TextComponent(text = '\n' + '您的成績:\n' + "至少要答對30題才可入榜" + '.' + userName + " 正確率:" + str(userRate/100) + '%', wrap = True)
      body_contents.append(text_user)
      if sexual == 0 or sexual == 1:
          hero_component = ImageComponent(
                                url = read_src_tori_jpg(),
                                size = "full")
      elif sexual == 2:
        hero_component = ImageComponent(
                              url = read_src_gongyoo_jpg(),
                              size = "full")
      elif sexual == 3:
        hero_component = ImageComponent(
                              url = read_src_squid_jpg(),
                              size = "full")
      elif sexual == 4:
        hero_component = ImageComponent(
                              url = read_src_dragon_jpg(),
                              size = "full")
      text_message = FlexSendMessage(
            alt_text='正確率風雲榜',
            contents= BubbleContainer(
                      header = BoxComponent(
                              layout = "vertical",
                              contents = [TextComponent(text = "正確率風雲榜\n(至少答對30題)", size = "3xl", align = "center", wrap = True)]
                                            ),
                      hero = hero_component,
                      body = BoxComponent(
                              layout = "vertical",
                              contents = body_contents
                                            ),
                      footer = BoxComponent(
                              layout = "horizontal",
                              contents = [ButtonComponent(style = "primary", action = MessageAction(label = "繼續挑戰", text = "答題"))]
                                            )
                      )

        )
      line_bot_api.reply_message(
      event.reply_token,
      text_message)
      return 0
    elif '掰掰精靈!' == text:
      print(event.source)
      d = json.loads(str(event.source))
      print(d['userId'])
      type_ = str(event.source)[2:6]
      if type_ == "grou":
        group_id = str(event.source)[13:46]
        line_bot_api.leave_group(group_id)
      elif type_ == "room":
        room_id = str(event.source)[12:45]
        line_bot_api.leave_room(room_id)
      else:
        img_src = read_src_mutom_jpg()
        line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(original_content_url= img_src,
                          preview_image_url= img_src))
        return 0



if __name__ == "__main__":
    port = int(os.environ['PORT'])
    app.run(host='0.0.0.0',port=port)