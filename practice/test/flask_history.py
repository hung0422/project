from flask import Flask , request ,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

class Config(object):
    '''配置參數'''
    #　sqlalchemy的配置參數
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost:3306/storedb"
    #　設置是否sqlalchemy自動追蹤資料庫的修改並發送訊號
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(Config)

# 創建資料庫sqlalchemy工具對象
db = SQLAlchemy(app)

@app.route('/test2/<userID>/<shoppingdate>' , methods=['GET'])
def test(userID,shoppingdate):

    sql = '''select p.productName,p.unitprice,s.quantity,p.unitprice*s.quantity as total 
            from shoppinglist s join product p
            on s.productID = p.productID
            where s.userID = '{}' and s.shoppingdate = '{}';'''.format(userID,shoppingdate)

    content = db.engine.execute(sql).fetchall()
    content_num = len(content)
    total = 0
    for i in content:
        total += int(i[3])

    return render_template('test2.html', content=content , total=total , content_num=content_num)


if __name__ == '__main__':
    app.debug = True
    app.run()