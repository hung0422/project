import pymysql, time, redis, json
from urllib.parse import parse_qs
from liffpy import LineFrontendFramework as LIFF
from flask import Flask, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from linebot.models.template import *
from linebot.models import *
# 引用自定義python
import transform, user_based_recommender

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)

# 引用無效簽章錯誤
from linebot.exceptions import (
    InvalidSignatureError
)

# 載入基礎設定檔
secretFileContentJson=json.load(open("./line_secret_key",'r',encoding='utf8'))
server_url=secretFileContentJson.get("server_url")

# 設定Server啟用細節
app = Flask(__name__,static_url_path = "/素材" , static_folder = "./素材/")

# 生成實體物件
line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))
handler = WebhookHandler(secretFileContentJson.get("secret_key"))

# liff
line_bot_token = secretFileContentJson.get("channel_access_token")
liff = LIFF(line_bot_token)

# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
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

# pymysql設定資料庫連線設定
host = 'mysql'
port = 3306
user = 'root'
passwd = 'iii'
db = 'storedb'

# SQLAlchemy設定資料庫連線設定
class Config(object):
    '''配置參數'''
    #　sqlalchemy的配置參數
    SQLALCHEMY_DATABASE_URI = "mysql://root:iii@mysql:3306/storedb"
    #　設置是否sqlalchemy自動追蹤資料庫的修改並發送訊號
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(Config)

# 創建資料庫sqlalchemy工具對象
db2 = SQLAlchemy(app)

# redis設定
redis = redis.StrictRedis(host='redis', port=6379, password='iii')

'''

消息判斷器

讀取指定的json檔案後，把json解析成不同格式的SendMessage

讀取檔案，
把內容轉換成json
將json轉換成消息
放回array中，並把array傳出。

'''


def detect_json_array_to_new_message_array(fileName):
    # 開啟檔案，轉成json
    with open(fileName, 'r', encoding='utf-8') as f:
        jsonArray = json.load(f)

    # 解析json
    returnArray = []
    for jsonObject in jsonArray:

        # 讀取其用來判斷的元件
        message_type = jsonObject.get('type')

        # 轉換
        if message_type == 'text':
            returnArray.append(TextSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'imagemap':
            returnArray.append(ImagemapSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'template':
            returnArray.append(TemplateSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'image':
            returnArray.append(ImageSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'sticker':
            returnArray.append(StickerSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'audio':
            returnArray.append(AudioSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'location':
            returnArray.append(LocationSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'flex':
            returnArray.append(FlexSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'video':
            returnArray.append(FlexSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'bubble':
            message_after = BubbleContainer.new_from_json_dict(jsonObject)
            returnArray.append(FlexSendMessage(alt_text="hello2", contents=message_after))

            # 回傳
    return returnArray


'''

handler處理關注消息

用戶關注時，讀取 素材 -> 關注 -> reply.json

將其轉換成可寄發的消息，傳回給Line

'''


# 關注事件處理
@handler.add(FollowEvent)
def process_follow_event(event):
    # 讀取並轉換
    result_message_array = []
    replyJsonPath = "素材/關注/reply.json"
    result_message_array = detect_json_array_to_new_message_array(replyJsonPath)

    # 消息發送
    line_bot_api.reply_message(
        event.reply_token,
        result_message_array
    )

    # 啟動第一張圖文選單
    linkRichMenuId = open("素材/" + 'rich_menu_0' + '/rich_menu_id', 'r').read()
    line_bot_api.link_rich_menu_to_user(event.source.user_id, linkRichMenuId)

    replyJsonPath = '素材/' + 'rich_menu_0' + "/reply.json"
    result_message_array = detect_json_array_to_new_message_array(replyJsonPath)

'''

handler處理文字消息

收到用戶回應的文字消息，
按文字消息內容，往素材資料夾中，找尋以該內容命名的資料夾，讀取裡面的reply.json

轉譯json後，將消息回傳給用戶

'''

# 文字消息處理
@handler.add(MessageEvent,message=TextMessage)
def process_text_message(event):

    # 讀取本地檔案，並轉譯成消息
    result_message_array =[]
    replyJsonPath = "素材/"+event.message.text+"/reply.json"
    result_message_array = detect_json_array_to_new_message_array(replyJsonPath)

    # 發送
    line_bot_api.reply_message(
        event.reply_token,
        result_message_array
    )


'''

handler處理Postback Event

載入功能選單與啟動特殊功能

解析postback的data，並按照data欄位判斷處理

現有三個欄位
menu, folder, tag

若folder欄位有值，則
    讀取其reply.json，轉譯成消息，並發送

若menu欄位有值，則
    讀取其rich_menu_id，並取得用戶id，將用戶與選單綁定
    讀取其reply.json，轉譯成消息，並發送

'''


@handler.add(PostbackEvent)
def process_postback_event(event):
    query_string_dict = parse_qs(event.postback.data)

    print(query_string_dict)
    if 'folder' in query_string_dict:

        result_message_array = []

        replyJsonPath = '素材/' + query_string_dict.get('folder')[0] + "/reply.json"
        result_message_array = detect_json_array_to_new_message_array(replyJsonPath)

        line_bot_api.reply_message(
            event.reply_token,
            result_message_array
        )
    elif 'menu' in query_string_dict:

        linkRichMenuId = open("素材/" + query_string_dict.get('menu')[0] + '/rich_menu_id', 'r').read()
        line_bot_api.link_rich_menu_to_user(event.source.user_id, linkRichMenuId)

        replyJsonPath = '素材/' + query_string_dict.get('menu')[0] + "/reply.json"
        result_message_array = detect_json_array_to_new_message_array(replyJsonPath)

        line_bot_api.reply_message(
            event.reply_token,
            result_message_array
        )

    # 取出用戶Line的userID及username並存到資料庫
    elif 'menu2' in query_string_dict:
        # 建立連線
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        # 建立游標
        cursor = conn.cursor()

        linkRichMenuId = open("素材/" + query_string_dict.get('menu2')[0] + '/rich_menu_id', 'r').read()
        line_bot_api.link_rich_menu_to_user(event.source.user_id, linkRichMenuId)

        # 取出消息內User的資料
        user_profile = line_bot_api.get_profile(event.source.user_id)

        # 將用戶資訊存在檔案內
        with open("./users.txt", "a") as myfile:
            myfile.write(json.dumps(vars(user_profile), sort_keys=True))
            myfile.write('\n')

        try:
            sql = '''
            INSERT INTO user_info (userID, name, regionID)
            VALUES ('{}','{}', 0);
            '''.format(str(user_profile.user_id), str(user_profile.display_name))

            cursor.execute(sql)
            conn.commit()

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="%s 您好!\n您可以點擊'常見問題'來查詢如何使用吾人能購" % (user_profile.display_name)))

        except pymysql.err.IntegrityError:
            print('Error', user_profile.user_id, 'existed.')
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="親愛的 %s 會員您好!\n感謝您回來繼續使用我們的服務" % (user_profile.display_name)))

        # 關閉游標及連線
        cursor.close()
        conn.close()

    # 從資料庫取出用戶的歷史交易紀錄五筆，並將詳細交易紀錄寫進網頁
    elif 'history' in query_string_dict:
        # 建立連線
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        # 建立游標
        cursor = conn.cursor()

        # 取出消息內User的資料
        user_profile = line_bot_api.get_profile(event.source.user_id)
        userID = str(user_profile.user_id)

        # 刪除過多的liff
        try:
            if len(liff.get()) >= 5:
                for i in range(len(liff.get())):
                    liff.delete(liff.get()[i]['liffId'])
        except:
            pass

        try:
            @app.route('/detail/<userID>/<shoppingdate>', methods=['GET'])
            def detail(userID, shoppingdate):

                shoppingdate = int(shoppingdate)
                shoppingdate = time.localtime(shoppingdate)
                shoppingdate = time.strftime("%Y-%m-%d %H:%M:%S", shoppingdate)

                sql = '''select p.productName,p.unitprice,s.quantity,p.unitprice*s.quantity as total 
                from shoppinglist s join product p
                on s.productID = p.productID
                where s.userID = '{}' and s.shoppingdate = '{}';'''.format(userID, shoppingdate)

                content = db2.engine.execute(sql).fetchall()
                content_num = len(content)
                total = 0
                for i in content:
                    total += int(i[3])

                return render_template('detail.html', content=content, total=total, content_num=content_num)
        except:
            pass

        sql = '''SELECT shoppingdate FROM shoppinglist 
        WHERE userID =  '{}' GROUP BY shoppingdate ORDER BY shoppingdate DESC LIMIT 5;
        '''.format(userID)

        cursor.execute(sql)
        data = cursor.fetchall()

        timestamp = []
        for j in range(len(data)):
            timestamp.append(int(time.mktime(time.strptime(str(data[j][0]), "%Y-%m-%d %H:%M:%S"))))

        # 產生liff網頁
        url = []
        liff_uri = []
        for i in range(len(timestamp)):
            url.append('{}'.format(server_url) + '/detail/' + '{}'.format(userID) + '/' + str(timestamp[i]))
        for liffuri in url:
            liff_uri.append('https://liff.line.me/' + liff.add(view_type="tall", view_url=liffuri))

        message_before = transform.transform_hist(data, liff_uri)
        message_after = BubbleContainer.new_from_json_dict(json.loads(message_before))
        message = FlexSendMessage(alt_text="hello2", contents=message_after)

        line_bot_api.reply_message(
            event.reply_token,
            message)

        # 關閉游標及連線
        cursor.close()
        conn.close()

    # 從資料庫取出用戶個人資料，並建立網頁供用戶修改資料，再存回資料庫
    elif 'information' in query_string_dict:
        # 建立連線
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        # 建立游標
        cursor = conn.cursor()

        # 取出消息內User的資料
        user_profile = line_bot_api.get_profile(event.source.user_id)
        userID = str(user_profile.user_id)

        # 刪除過多的liff
        try:
            if len(liff.get()) >= 5:
                for i in range(len(liff.get())):
                    liff.delete(liff.get()[i]['liffId'])
        except:
            pass

        # 建立網頁並將修改完後的資料存回資料庫
        try:
            @app.route('/change/<userID>', methods=['GET'])
            def change(userID):
                return render_template('change.html', ID=userID)

            @app.route('/submit', methods=['POST'])
            def submit():
                user_ID = request.values['user_ID']
                name = request.values['name']
                gender = request.values['gender']
                regionID = request.values['regionID']
                email = request.values['email']

                sql = '''UPDATE user_info 
                    SET name = '{}', gender = '{}', regionID = '{}', email = '{}'
                    WHERE userID = '{}';'''.format(name, gender, regionID, email, user_ID)

                db2.engine.execute(sql)

                if gender == 'male':
                    flask_gender = '男'
                else:
                    flask_gender = '女'

                if regionID == '320':
                    flask_region = '中壢區'
                elif regionID == '324':
                    flask_region = '平鎮區'
                elif regionID == '325':
                    flask_region = '龍潭區'
                elif regionID == '326':
                    flask_region = '楊梅區'
                elif regionID == '327':
                    flask_region = '新屋區'
                elif regionID == '328':
                    flask_region = '觀音區'
                elif regionID == '330':
                    flask_region = '桃園區'
                elif regionID == '333':
                    flask_region = '龜山區'
                elif regionID == '334':
                    flask_region = '八德區'
                elif regionID == '335':
                    flask_region = '大溪區'
                elif regionID == '336':
                    flask_region = '復興區'
                elif regionID == '337':
                    flask_region = '大園區'
                elif regionID == '338':
                    flask_region = '蘆竹區'
                output = '''
                <html>
                    <head>
                        <title>會員中心</title>
                    </head>
                    <body>
                            <div>
                                <font size=32 > <center> <b>您已將資料更改如下 </b> </center> </font>
                            </div>
                                <br>
                            <div>
                                <font size=32 > <center> 姓名: %s </center> </font>
                            </div>
                                <br>
                            <div>
                                <font size=32 > <center> 性別: %s </center> </font>
                            </div>
                                <br>
                            <div>
                                <font size=32 > <center> 地區: %s </center> </font>
                            </div>
                                <br>
                            <div>
                                <font size=32 > <center> email: %s </center> </font>
                            </div>
                                <br>
                    </body>
                </html>
                ''' % (name, flask_gender, flask_region, email)

                return output
        except:
            pass

    # 將暫時交易紀錄寫進網頁
    elif 'shopping_cart' in query_string_dict:

        # 取出消息內User的資料
        user_profile = line_bot_api.get_profile(event.source.user_id)
        userID = str(user_profile.user_id)

        # 刪除過多的liff
        try:
            if len(liff.get()) >= 5:
                for i in range(len(liff.get())):
                    liff.delete(liff.get()[i]['liffId'])
        except:
            pass

        try:
            @app.route('/shopcar/<userID>', methods=['GET'])
            def shopcar(userID):
                try:
                    redis_get = redis.get('{}'.format(userID))
                    content = redis_get.decode('utf-8').split(',')
                    content_num = len(content)
                    total = 0
                    for i in content:
                        total += int(i.split(':')[3])

                    return render_template('shopcar.html', content=content, total=total, content_num=content_num)
                except:
                    total = 0
                    return render_template('shopcar_empty.html', total=total)
        except:
            pass

        # 產生liff網頁
        url = '{}'.format(server_url) + '/shopcar/' + '{}'.format(userID)
        liff_uri = 'https://liff.line.me/' + liff.add(view_type="tall", view_url=url)

        message_before = transform.transform_shopcar(liff_uri)
        message_after = BubbleContainer.new_from_json_dict(json.loads(message_before))
        message = FlexSendMessage(alt_text="hello3", contents=message_after)
        line_bot_api.reply_message(
            event.reply_token,
            message)

    # 推薦商品
    elif 'recommender' in query_string_dict:

        # 建立連線
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        # 建立游標
        cursor = conn.cursor()

        # 取出消息內User的資料
        user_profile = line_bot_api.get_profile(event.source.user_id)
        userID = str(user_profile.user_id)

        price = []
        data = user_based_recommender.main('1')  # userID
        for i in data:
            sql = '''select unitprice from product where productName ='{}';'''.format(i)
            cursor.execute(sql)
            i_price = cursor.fetchall()[0][0]
            price.append(i_price)

        print(data)
        print(price)
        message_before = transform.transform_recom(data, price)
        message_after = CarouselContainer.new_from_json_dict(json.loads(message_before))
        message = FlexSendMessage(alt_text="oh", contents=message_after)
        line_bot_api.reply_message(
            event.reply_token,
            message)

        # 關閉游標及連線
        cursor.close()
        conn.close()

    # 常見問題
    elif 'question' in query_string_dict:

        # 創建QuickReplyButton
        # 點擊後，以Postback事件回應Server
        shopcarButton = QuickReplyButton(
            action=PostbackAction(label="購物車", data="folder=problem_shopcar")
        )
        recomButton = QuickReplyButton(
            action=PostbackAction(label="推薦商品", data="folder=problem_recom")
        )
        histButton = QuickReplyButton(
            action=PostbackAction(label="交易紀錄", data="folder=problem_hist")
        )
        discountButton = QuickReplyButton(
            action=PostbackAction(label="最新優惠", data="folder=problem_discount")
        )
        infoButton = QuickReplyButton(
            action=PostbackAction(label="會員中心", data="folder=problem_info")
        )
        # 設計QuickReplyButton的List
        quickReplyList = QuickReply(
            items=[shopcarButton, recomButton, histButton, discountButton, infoButton]
        )

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='想問甚麼功能?', quick_reply=quickReplyList))


'''

若收到圖片消息時，

先回覆用戶文字消息，並從Line上將照片拿回。

'''

message_before = transform.transform_start()
message_after = BubbleContainer.new_from_json_dict(json.loads(message_before))
message = FlexSendMessage(alt_text="haha", contents=message_after)


@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        message)
    message_content = line_bot_api.get_message_content(event.message.id)
    with open('./素材/images/' + event.message.id + '.jpg', 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

# 成功辨識出人臉後，向該會員傳送歡迎訊息
@app.route("/welcome/<userID>", methods=['GET'])
def pushWelcom(userID):
    try:
        line_bot_api.push_message(userID,
                                  [
                                      TextSendMessage(text="歡迎光臨無人能購!\n點擊'購物車'來查看本次交易的即時購買情形\n祝您購物愉快!"),
                                  ]
                                 )
    except :
        print('Push Error.')

# 結束交易後，向該會員傳送交易結束訊息
@app.route("/thank/<userID>", methods=['GET'])
def pushthank(userID):
    try:
        line_bot_api.push_message(userID,
                                  [
                                      TextSendMessage(text="感謝您的光臨!\n點擊'交易紀錄'來查看最新紀錄"),
                                  ]
                                 )
    except :
        print('Push Error.')

'''

Application 運行（開發版）

'''
if __name__ == "__main__":
    app.run(host='0.0.0.0')

'''

Application 運行（heroku版）

'''
# import os
# if __name__ == "__main__":
#     app.run(host='0.0.0.0',port=os.environ['PORT'])