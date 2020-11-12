from flask import Flask , request ,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

class Config(object):
    '''配置參數'''
    #　sqlalchemy的配置參數
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost:3306/linebot"
    #　設置是否sqlalchemy自動追蹤資料庫的修改並發送訊號
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(Config)

# 創建資料庫sqlalchemy工具對象
db = SQLAlchemy(app)



@app.route('/html2/<userID>' , methods=['GET'])
def html2(userID):
    return render_template('html2.html' , ID = userID)
@app.route('/submit', methods =['POST'])
def submit():
    user_ID = request.values['user_ID']
    name = request.values['name']
    gender = request.values['gender']
    region_id = request.values['region_id']


    # sql = '''UPDATE customer_info
    #         SET name = '{}', gender = '{}', age = '{}', creditcardNO = '{}', securitycode = '{}'
    #         WHERE userID = '{}';'''.format(name,gender,age,creditcardNO,securitycode,user_ID)
    #
    # db.engine.execute(sql)

    if gender == 'male':
        flask_gender = '男'
    else:
        flask_gender = '女'
    if region_id == '320':
        flask_region = '中壢區'
    elif region_id == '324':
        flask_region = '平鎮區'
    elif region_id == '325':
        flask_region = '龍潭區'
    elif region_id == '326':
        flask_region = '楊梅區'
    elif region_id == '327':
        flask_region = '新屋區'
    elif region_id == '328':
        flask_region = '觀音區'
    elif region_id == '330':
        flask_region = '桃園區'
    elif region_id == '333':
        flask_region = '龜山區'
    elif region_id == '334':
        flask_region = '八德區'
    elif region_id == '335':
        flask_region = '大溪區'
    elif region_id == '336':
        flask_region = '復興區'
    elif region_id == '337':
        flask_region = '大園區'
    elif region_id == '338':
        flask_region = '蘆竹區'
    output = '''
    <html lang="en">
        <head>
            <title>test</title>
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
        </body>
    </html>
    '''%(name,flask_gender,flask_region)

    return output


if __name__ == '__main__':
    app.debug = True
    app.run()