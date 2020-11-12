from flask import Flask , request ,render_template
import redis

r = redis.StrictRedis(host='192.168.136.129', port=6379, password='iii')
app = Flask(__name__)


a = r.get('foo')
frult = a.decode('utf-8').split(',')
frult0 = frult[0].split(':')
frult1 = frult[1].split(':')

message = """"""
message += """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>test123</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link href="'style.css" rel="stylesheet" type="text/css" />
</head>
<body>
    <div>
        <div>
            <table class="table">
                <thead>
                    <tr class="danger">
                        <th>product</th>
                        <th>amount</th>
                        <th>price</th>
                        <th>total</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="success">
                        <td> %s</td>
                        <td> %s</td>
                        <td> %s</td>
                        <td> %s</td>
                    </tr>
                    <tr class="warning">
                        <td> %s</td>
                        <td> %s</td>
                        <td> %s</td>
                        <td> %s</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>"""%(frult0[0],frult0[1],frult0[2],int(frult0[1])*int(frult0[2]),frult1[0],frult1[1],frult1[2],int(frult1[1])*int(frult1[2]))

with open('./templates/test2','w',encoding='utf-8') as f:
    f.write(message)

@app.route('/' , methods=['GET'])
def table():
    message2 = """"""
    with open('./templates/test2', 'r', encoding='utf-8') as h:
        message2 = h.read()
    return message2

if __name__ == '__main__':
    app.debug = True
    app.run()