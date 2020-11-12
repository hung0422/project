'''
        message = TemplateSendMessage(
        alt_text='confirm template',
        template=ConfirmTemplate(
        title='ConfirmTemplate',
        text='您是否要更改您的個人資料?',
            actions=[
                URITemplateAction(
                    label='是',
                    uri= liff_uri
                ),
                MessageTemplateAction(
                    label='否',
                    text="我沒有要更改個人資料"
                    )
                ]
            )
        )

        line_bot_api.reply_message(
                    event.reply_token,[
                    TextSendMessage(text="{}".format(final_data)),
                    message])
'''

'''
def transform_info(name,gender,age,card,url):
    message = FlexSendMessage(
        alt_text='hello',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "會員中心",
                        "weight": "bold",
                        "size": "xxl",
                        "align": "center",
                        "contents": []
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "姓名",
                        "weight": "bold",
                        "size": "xl",
                        "align": "start",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": "{}".format(name),
                        "size": "sm",
                        "margin": "xs",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": "性別",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "md",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": "{}".format(gender),
                        "margin": "sm",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": "年齡",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "md",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": "{}".format(age),
                        "margin": "sm",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": "信用卡卡號",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "md",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": "{}".format(card),
                        "margin": "sm",
                        "contents": []
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "更改資料",
                            "uri": "{}".format(url)
                        },
                        "color": "#905C44FF",
                        "style": "primary"
                    }
                ]
            }
        })
    return message
'''

'''
def transform_recom2(data):
    temporary_message = """"""
    for i in range(len(data)):
        temporary_message += """
              {
        "type": "text",
        "text": "%s",
        "size": "xl",
        "align": "center",
        "margin": "md",
        "wrap": true,
        "contents": []
      }"""%(data[i])
        if i < len(data) - 1:
            temporary_message += ""","""
    message = """
    {
  "type": "bubble",
  "direction": "ltr",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "商品推薦",
        "weight": "bold",
        "size": "3xl",
        "align": "center",
        "contents": []
      }
    ]
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [%s]
      }
    }"""%(temporary_message)
    return message
'''
'''
# message = TemplateSendMessage(
#     alt_text='Buttons template',
#     template=ButtonsTemplate(
#         #thumbnail_image_url='https://example.com/image.jpg',
#         title='最後一步',
#         text='點擊按鈕開始使用服務',
#         actions=[
#             PostbackTemplateAction(
#                 type= "postback",
#                 label='正式使用無人能購',
#                 text='啟動服務',
#                 data='menu2=rich_menu_1'
#             )
#         ]
#     )
# )
'''