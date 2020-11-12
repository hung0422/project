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



@app.route('/html1/<userID>' , methods=['GET'])
def html2(userID):
    return render_template('html1.html' , ID = userID)
@app.route('/submit', methods =['POST'])
def submit():
    user_ID = request.values['user_ID']
    name = request.values['name']
    gender = request.values['gender']
    age = request.values['age']
    creditcardNO = request.values['creditcardNO']
    securitycode = request.values['securitycode']

    sql = '''UPDATE customer_info
            SET name = '{}', gender = '{}', age = '{}', creditcardNO = '{}', securitycode = '{}'
            WHERE userID = '{}';'''.format(name,gender,age,creditcardNO,securitycode,user_ID)

    db.engine.execute(sql)
    return '資料更改完成'


if __name__ == '__main__':
    app.debug = True
    app.run()

#<p><input type = 'textbox'   class='form-control' style="font-size:16px;padding:100px"  name = 'work'  placeholder="請詳述您的工作經歷"></p>
#http://127.0.0.1:5000/html2