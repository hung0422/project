from flask import Flask
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

userID = 'U4bfc7d1887075bbeebbee8c819ab8838'

@app.route('/<userID>' , methods=['GET'])
def index(userID):
    sql_cmd = """
            select * from customer_info where userID = '{}'
            """.format(userID)

    query_data = db.engine.execute(sql_cmd)
    data = query_data.fetchmany(1)
    data2 = data[0][1]
    print(data)
    print(type(data))
    print(data2)
    #print(query_data.name)
    return data2


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)