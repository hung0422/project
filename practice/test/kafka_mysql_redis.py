import pymysql
import redis
import time

# redis = redis.StrictRedis(host='192.168.1.24', port=6379, password='iii')
#
host = 'localhost'
port = 3306
user = 'root'
passwd = 'root'
db = 'storedb'


conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)

cursor = conn.cursor()
#
# message = ''
#
kafka_test = 'Ub52d90a6b2c9b05bed228af9d7538a6b'
# kafka_test2 = '鴻津太國捲(蛋奶素)-370g 樂米穀場花東自然農耕特哉鮮白米(圓二)1.5K 一匙靈Attack抗菌EX洗衣精補充-1.5Kg'
# kafka_test3 = kafka_test2.split(' ')
# print(kafka_test3)
# for i in range(len(kafka_test3)):
#     sql = '''select unitprice from product where productName = '{}';'''.format(kafka_test3[i])
#     cursor.execute(sql)
#     data = cursor.fetchall()[0][0]
#     message += '{}:{}:{}:{}'.format(kafka_test3[i],data,1,data*1)
#     if i < len(kafka_test3) - 1:
#         message += ','
#
# cursor.close()
# conn.close()
#
# print(message)
# redis.set(kafka_test,message)

qqq = (1, 1603711396293)[1]/1000
qqq = time.localtime(qqq)
qqq = time.strftime("%Y-%m-%d %H:%M:%S", qqq)
print(qqq)

www = ['樂米穀場花東自然農耕特哉鮮白米(圓二)1.5K:189:1:189', '中興米外銷日本之米(圓ㄧ)3Kg:169:1:169']

for i in www:
    sql = '''select productID from product where productName = '{}';'''.format(i.split(':')[0])
    cursor.execute(sql)
    data = cursor.fetchall()[0][0]
    sql2 = '''INSERT INTO shoppinglist (userID,shoppingdate,productID,quantity) VALUE ('{}','{}','{}',1);'''.format(kafka_test,qqq,data)
    cursor.execute(sql2)
    conn.commit()

cursor.close()
conn.close()