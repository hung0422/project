def transform_info(name,gender,regionID,email,url):
    message = """{
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
        "size": "3xl",
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
        "text": "%s",
        "size": "xxl",
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
        "text": "%s",
        "size": "xxl",
        "margin": "sm",
        "contents": []
      },
      {
        "type": "text",
        "text": "地區",
        "weight": "bold",
        "size": "xl",
        "margin": "md",
        "contents": []
      },
      {
        "type": "text",
        "text": "%s",
        "size": "xxl",
        "margin": "sm",
        "contents": []
      },
      {
        "type": "text",
        "text": "email",
        "weight": "bold",
        "size": "xl",
        "margin": "md",
        "contents": []
      },
      {
        "type": "text",
        "text": "%s",
        "size": "xxl",
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
          "uri": "%s"
        },
        "color": "#905C44FF",
        "style": "primary"
      }
    ]
  }
}"""%(name,gender,regionID,email,url)
    return message

def transform_hist(data,url):
    temporary_message = """"""
    if len(data) == 0:
        temporary_message = """{
        "type": "text",
        "text": "您還沒有進行任何交易呦!!",
        "weight": "bold",
        "size": "xl",
        "align": "center",
        "wrap": true,
        "decoration": "underline",
        "contents": []
        }"""
    else:
        for i in range(len(data)):
            temporary_message += """{
            "type": "text",
            "text": "%s",
            "weight": "bold",
            "size": "xl",
            "align": "center",
            "margin": "md",
            "action": {
              "type": "uri",
              "uri": "%s"
            },
            "contents": []
            }"""%(data[i][0].strftime('%Y-%m-%d %H:%M:%S'),url[i])
            if i < len(data) - 1:
                temporary_message += ""","""
    message = """{
  "type": "bubble",
  "direction": "ltr",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "交易紀錄",
        "weight": "bold",
        "size": "3xl",
        "align": "center",
        "contents": []
      },
      {
        "type": "text",
        "text": "點選日期查看詳細記錄",
        "weight": "bold",
        "size": "xl",
        "align": "center",
        "gravity": "bottom",
        "margin": "xxl",
        "wrap": false,
        "style": "normal",
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

def transform_shopcar(url):
    message = """{
      "type": "bubble",
      "direction": "ltr",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "購物車",
            "weight": "bold",
            "size": "3xl",
            "align": "center",
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
              "label": "查看購物車",
              "uri": "%s"
            },
            "color": "#905C44FF",
            "style": "primary"
          }
        ]
      }
    }"""%(url)
    return message

def transform_start():
    message = """{
  "type": "bubble",
  "direction": "ltr",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "啟動服務",
        "weight": "bold",
        "size": "3xl",
        "align": "center",
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
          "type": "postback",
          "label": "正式使用吾人能購",
          "text": "啟動服務",
          "data": "menu2=rich_menu_1"
        },
        "color": "#905C44FF",
        "style": "primary"
      }
    ]
  }
}"""
    return message



def transform_recom(data,price):
    temporary_message = """"""
    for i in range(len(data)):
        temporary_message += """
        {
  "type": "bubble",
  "direction": "ltr",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "商品",
        "weight": "bold",
        "size": "xl",
        "align": "start",
        "margin": "md",
        "contents": []
      },
      {
        "type": "text",
        "text": "%s",
        "size": "xxl",
        "margin": "md",
        "wrap": true,
        "contents": []
      },
      {
        "type": "text",
        "text": "價格",
        "weight": "bold",
        "size": "xl",
        "margin": "md",
        "contents": []
      },
      {
        "type": "text",
        "text": "%s",
        "size": "xxl",
        "margin": "md",
        "contents": []
      }
    ]
  }
}"""%(data[i],price[i])
        if i < len(data) - 1:
            temporary_message += ""","""
    message = """
    {
  "type": "carousel",
  "contents": [%s]
}"""%(temporary_message)
    return message

def transform_recom_empty():
    message = """
    {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "direction": "ltr",
      "hero": {
        "type": "image",
        "url": "https://image.azureedge.net/0096819_3kg.jpeg",
        "size": "full",
        "aspectRatio": "1.51:1",
        "aspectMode": "fit"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "商品",
            "weight": "bold",
            "size": "xl",
            "align": "start",
            "margin": "md",
            "contents": []
          },
          {
            "type": "text",
            "text": "中興米外銷日本之米(圓ㄧ)3Kg",
            "size": "xxl",
            "margin": "md",
            "wrap": true,
            "contents": []
          },
          {
            "type": "text",
            "text": "價格",
            "weight": "bold",
            "size": "xl",
            "margin": "md",
            "contents": []
          },
          {
            "type": "text",
            "text": "169",
            "size": "xxl",
            "margin": "md",
            "contents": []
          }
        ]
      }
    },
    {
      "type": "bubble",
      "direction": "ltr",
      "hero": {
        "type": "image",
        "url": "https://a.ecimg.tw/items/DBACD619008AZ8A/000001_1501224749.jpg",
        "size": "full",
        "aspectRatio": "1.51:1",
        "aspectMode": "fit"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "商品",
            "weight": "bold",
            "size": "xl",
            "align": "start",
            "margin": "md",
            "contents": []
          },
          {
            "type": "text",
            "text": "鴻津太國捲(蛋奶素)-370g",
            "size": "xxl",
            "margin": "md",
            "wrap": true,
            "contents": []
          },
          {
            "type": "text",
            "text": "價格",
            "weight": "bold",
            "size": "xl",
            "margin": "md",
            "contents": []
          },
          {
            "type": "text",
            "text": "88",
            "size": "xxl",
            "margin": "md",
            "contents": []
          }
        ]
      }
    },
    {
      "type": "bubble",
      "direction": "ltr",
      "hero": {
        "type": "image",
        "url": "https://image.azureedge.net/0192542_300g.jpeg",
        "size": "full",
        "aspectRatio": "1.51:1",
        "aspectMode": "fit"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "商品",
            "weight": "bold",
            "size": "xl",
            "align": "start",
            "margin": "md",
            "contents": []
          },
          {
            "type": "text",
            "text": "安心雞-清胸肉",
            "size": "xxl",
            "margin": "md",
            "wrap": true,
            "contents": []
          },
          {
            "type": "text",
            "text": "價格",
            "weight": "bold",
            "size": "xl",
            "margin": "md",
            "contents": []
          },
          {
            "type": "text",
            "text": "69",
            "size": "xxl",
            "margin": "md",
            "contents": []
          }
        ]
      }
    },
    {
      "type": "bubble",
      "direction": "ltr",
      "hero": {
        "type": "image",
        "url": "https://image.azureedge.net/0091181_1857ml.jpeg",
        "size": "full",
        "aspectRatio": "1.51:1",
        "aspectMode": "fit"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "商品",
            "weight": "bold",
            "size": "xl",
            "align": "start",
            "margin": "md",
            "contents": []
          },
          {
            "type": "text",
            "text": "林鳳營低脂鮮乳1857ml",
            "size": "xxl",
            "margin": "md",
            "wrap": true,
            "contents": []
          },
          {
            "type": "text",
            "text": "價格",
            "weight": "bold",
            "size": "xl",
            "margin": "md",
            "contents": []
          },
          {
            "type": "text",
            "text": "166",
            "size": "xxl",
            "margin": "md",
            "contents": []
          }
        ]
      }
    },
    {
      "type": "bubble",
      "direction": "ltr",
      "hero": {
        "type": "image",
        "url": "https://s.yimg.com/zp/MerchandiseImages/9122EDF45B-Product-21304883.jpg",
        "size": "full",
        "aspectRatio": "1.51:1",
        "aspectMode": "fit"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "商品",
            "weight": "bold",
            "size": "xl",
            "align": "start",
            "margin": "md",
            "contents": []
          },
          {
            "type": "text",
            "text": "一匙靈Attack抗菌EX洗衣精補充-1.5Kg",
            "size": "xxl",
            "margin": "md",
            "wrap": true,
            "contents": []
          },
          {
            "type": "text",
            "text": "價格",
            "weight": "bold",
            "size": "xl",
            "margin": "md",
            "contents": []
          },
          {
            "type": "text",
            "text": "79",
            "size": "xxl",
            "margin": "md",
            "contents": []
          }
        ]
      }
    }
  ]
}"""
    return message