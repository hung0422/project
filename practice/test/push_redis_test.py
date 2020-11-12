import redis

redis = redis.StrictRedis(host='192.168.1.24', port=6379, password='iii')

# a = 'hello'
# b = 'apple:10:1:10,banana:20:2:40'
#
# redis.set(a,b)
# print('OK')

ID = 'Ub52d90a6b2c9b05bed228af9d7538a6b'

ccc = redis.get('{}'.format(ID))
content = ccc.decode('utf-8').split(',')
print(content)