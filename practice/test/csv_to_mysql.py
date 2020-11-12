import csv, pymysql

host = 'localhost'
port = 3306
user = 'root'
passwd = 'root'
db = 'storedb'

conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
cursor = conn.cursor()


with open('1027.csv',newline='') as f:
    aaa = csv.reader(f)

    for i in aaa:
        print(i)
        sql = '''INSERT INTO product (productID,productName,categoryName,unitprice) VALUE ('{}','{}','{}','{}');'''.format(i[0],i[1],i[2],i[3])
        cursor.execute(sql)

    conn.commit()
    cursor.close()
    conn.close()