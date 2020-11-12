import pymysql

host = 'localhost'
port = 3306
user = 'root'
passwd = 'root'
db = 'linebot'
#charset = 'utf8mp4'

conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)

cursor = conn.cursor()

aaa = 'qweqwe'
bbb = 'TOM'

# sql = '''
#     INSERT INTO customer_info (userID, name)
#     VALUES ('{}','{}');
#     '''.format(aaa,bbb)
#
# cursor.execute(sql)
# conn.commit()
#############################################################
# sql = '''select name from customer_info where userID = "{}";'''.format(aaa)
# cursor.execute(sql)
#
# data = cursor.fetchmany(1)
# data2 = data[0][0]
# print(data2)
############################################################
# zzz = 'Uc6e8a46ba4671183c1c8474b50ae141b'
# sql = '''select shoppingdate,totalprice from shoppinglist where userID =  '{}' ORDER BY shoppingdate DESC LIMIT 5;'''.format(zzz)
# # sql = '''select s.shoppingdate,s.totalprice,p.productname,i.amount from shoppinglist s join product p join itemlist i
# # on s.shoppinglistID = i.shoppinglistID and i.productID = p.productID where s.userID = '{}';'''.format(zzz)
# cursor.execute(sql)
# data = cursor.fetchall()
#
# message = ''
# print(data)
# for i in range(0,len(data)):
#     data1 = data[i][1]
#     data1 = str(data1)
#     data2 = data[i][0]
#     data2 = data2.strftime('%Y-%m-%d')
#     data3 = data2 +' '+ data1
#     message = message + data3 + '\n'
#
# if message == '':
#     print('您還沒有進行任何交易')
# else:
#     print(message)
# cursor.close()
# conn.close()
#################################################

# zzz = 'Uc6e8a46ba4671183c1c8474b50ae141b'
# sql = '''select shoppingdate,totalprice from shoppinglist where userID =  '{}' ORDER BY shoppingdate DESC LIMIT 5;'''.format(zzz)
# # sql = '''select s.shoppingdate,s.totalprice,p.productname,i.amount from shoppinglist s join product p join itemlist i
# # on s.shoppinglistID = i.shoppinglistID and i.productID = p.productID where s.userID = '{}';'''.format(zzz)
# cursor.execute(sql)
# data = cursor.fetchall()
# print(data)
# if data == ():
#     print('您還沒有進行任何交易')
# else:
#     for i in range(0, len(data)):
#         data0 = data[0][0].strftime('%Y-%m-%d') + ' ' + '共花費' + str(data[0][1]) + '元'
#         data1 = data[1][0].strftime('%Y-%m-%d') + ' ' + '共花費' + str(data[1][1]) + '元'
#         data2 = data[2][0].strftime('%Y-%m-%d') + ' ' + '共花費' + str(data[2][1]) + '元'
#         data3 = data[3][0].strftime('%Y-%m-%d') + ' ' + '共花費' + str(data[3][1]) + '元'
#         data4 = data[4][0].strftime('%Y-%m-%d') + ' ' + '共花費' + str(data[4][1]) + '元'
#         print(data0)
#         print(data1)
#         print(data2)
#         print(data3)
#         print(data4)
# message = ''
# for i in range(0, len(data)):
#     message += data[i][0].strftime('%Y-%m-%d') + ' ' + '共花費' + str(data[i][1]) + '元'
############################################################

cursor.close()
conn.close()

