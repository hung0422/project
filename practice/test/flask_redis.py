import redis
from flask import Flask , request ,render_template


r = redis.StrictRedis(host='192.168.1.24', port=6379, password='iii')

app = Flask(__name__)
@app.route('/' , methods=['GET'])
def redis():
    a = r.get('foo')
    b = a.decode('utf-8')
    return b

@app.route('/test/<userID>' , methods=['GET'])
def test(userID):
    try:
        a = r.get('{}'.format(userID))
        content = a.decode('utf-8').split(',')
        content_num = len(content)
        total = 0
        for i in content:
            total += int(i.split(":")[3])

        return render_template('test.html', content=content , total=total , content_num=content_num)
    except:
        total = 0
        return render_template('test3.html', total=total)

if __name__ == '__main__':
    app.debug = True
    app.run()

# a = r.get('foo')
# frult = a.decode('utf-8').split(',')
# print(frult)
# # frult0 = frult[0].split(':')
# # frult1 = frult[1].split(':')
# # # for i in frult:
# # #     print(i)
# # #     for j in i.split(':'):
# # #         print(j)
# # # print(frult0)
# # # print(frult1)
# # aaa = 0
# # for q in range(len(frult)):
# #     # print(q+1)
# #     # print(frult[q].split(":")[3])
# #     # aaa += int(frult[q].split(":")[3])
# #     for w in frult[q].split(':'):
# #         print(w)
# # print(aaa)