import pymysql

host = '192.168.1.24'
port = 3307
user = 'root'
passwd = 'iii'
db = 'storedb'

conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
cursor = conn.cursor()

sql = '''select shoppingdate from shoppinglist where userID = 'Ub52d90a6b2c9b05bed228af9d7538a6b' group by shoppingdate;'''

cursor.execute(sql)

data = cursor.fetchall()
print(data)
print(len(data))
cursor.close()
conn.close()