import pymysql
import time

host = 'localhost'
port = 3306
user = 'root'
passwd = 'root'
db = 'storedb'

userID = 'Ub52d90a6b2c9b05bed228af9d7538a6b'
shoppingdate = '2020-10-20 09:30:35'
conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)

cursor = conn.cursor()

# sql = '''select p.productName,p.unitprice,s.quantity,p.unitprice*s.quantity as total
#         from shoppinglist s join product p
#         on s.productID = p.productID
#         where s.userID = '{}' and s.shoppingdate = '{}';'''.format(userID, shoppingdate)
#
# cursor.execute(sql)
#
# data = cursor.fetchall()
#
# print(data)
#
# cursor.close()
# conn.close()
###############################################

# sql = '''SELECT shoppingdate FROM shoppinglist
#         WHERE userID =  '{}' GROUP BY shoppingdate ORDER BY shoppingdate DESC LIMIT 5;'''.format(userID)
#
# cursor.execute(sql)
# data = cursor.fetchall()
# print(data)
# zzz = data[0][0]
# print(zzz)
# print(type(zzz))
#
# aaa = []
# for i in range(len(data)):
#     aaa.append(int(time.mktime(time.strptime(str(data[i][0]),"%Y-%m-%d %H:%M:%S"))))
#
# url = []
# for o in range(len(aaa)):
#     url.append('http://127.0.0.1:5000' + '/test2/' + '{}'.format(userID) + '/' +str(aaa[o]))
# print(url)
#
#
# a = aaa[0]
# print(a)
# print(type(a))
# print('=============')
# a = time.localtime(a)
# print(a)
# print(type(a))
# print('===========================')
# a = time.strftime("%Y-%m-%d %H:%M:%S", a)
# print(a)
# print(type(a))
#
# #
# for j in url:
#     print(j)

#########################################
xxx = ['三好米ㄧ等壽司米(圓一)2.7kg', '農心醡醬風味麵(包)140g', 'St.Michel巧克力奶油餅-150g', '英國Barr覆盆子風味無糖飲料-330ml', 'PMU熊寶貝 素色舒柔墊9入-淺藍 32*32*1cm']
price = []
for i in xxx:
    sql = '''select unitprice from product where productName ='{}';'''.format(i)

    cursor.execute(sql)
    data = cursor.fetchall()[0][0]
    price.append(data)
print(price)
for o in price:
    print(o)

cursor.close()
conn.close()