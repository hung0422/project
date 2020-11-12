import pymysql

host = 'localhost'
port = 3306
user = 'root'
passwd = 'root'
db = 'linebot'

userID = 'qweqwe'

conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)

cursor = conn.cursor()

sql = '''SELECT name,gender,age,creditcardNO,securitycode from customer_info where userID = "{}";'''.format(userID)

cursor.execute(sql)

data = cursor.fetchmany(1)
data0 = '名字:' + str(data[0][0]) + '\n'
data1 = str(data[0][1])
if data1 == '1':
    data1 = '男'
elif data1 == '2':
    data1 = '女'
data1 = '性別:' + data1 +'\n'
data2 = '年齡:' + str(data[0][2]) + '\n'
data3 = '信用卡卡號:' + str(data[0][3])+ '\n'
data4 = '信用卡檢查碼:' +str(data[0][4])
message = data0 + data1 + data2 +data3 + data4

print(message)


cursor.close()
conn.close()

