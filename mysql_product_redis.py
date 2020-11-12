import pymysql, redis

host = 'mysql'
port = 3306
user = 'root'
passwd = 'iii'
db = 'storedb'

conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
cursor = conn.cursor()

redis = redis.StrictRedis(host='redis', port=6379, password='iii')

sql = '''select productName,unitprice from product;'''

cursor.execute(sql)
data = cursor.fetchall()

for i in data:
    product = i[0]
    price = i[1]
    redis.set(product,price)

cursor.close()
conn.close()
print('OK')