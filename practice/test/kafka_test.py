from confluent_kafka import Consumer, KafkaException, KafkaError
import sys, pymysql , redis, time, requests

redis = redis.StrictRedis(host='192.168.1.24', port=6379, password='iii')

host = 'localhost'
port = 3306
user = 'root'
passwd = 'root'
db = 'storedb'

conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
cursor = conn.cursor()

# 用來接收從Consumer instance發出的error訊息
def error_cb(err):
    print('Error: %s' % err)


# 轉換msgKey或msgValue成為utf-8的字串
def try_decode_utf8(data):
    if data:
        return data.decode('utf-8')
    else:
        return None


# 當發生Re-balance時, 如果有partition被assign時被呼叫
def print_assignment(consumer, partitions):
    result = '[{}]'.format(','.join([p.topic + '-' + str(p.partition) for p in partitions]))
    print('Setting newly assigned partitions:', result)


# 當發生Re-balance時, 之前被assigned的partition會被移除
def print_revoke(consumer, partitions):
    result = '[{}]'.format(','.join([p.topic + '-' + str(p.partition) for p in partitions]))
    print('Revoking previously assigned partitions: ' + result)


if __name__ == '__main__':
    # 步驟1.設定要連線到Kafka集群的相關設定
    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    props = {
        'bootstrap.servers': '192.168.1.24:9092',         # Kafka集群在那裡? (置換成要連接的Kafka集群)
        'group.id': 'iii',                             # ConsumerGroup的名稱 (置換成你/妳的學員ID)
        'auto.offset.reset': 'earliest',               # Offset從最前面開始
        'error_cb': error_cb                           # 設定接收error訊息的callback函數
    }

    # 步驟2. 產生一個Kafka的Consumer的實例
    consumer = Consumer(props)
    # 步驟3. 指定想要訂閱訊息的topic名稱
    topicName = 'Shopping_list2'
    # 步驟4. 讓Consumer向Kafka集群訂閱指定的topic
    consumer.subscribe([topicName], on_assign=print_assignment, on_revoke=print_revoke)

    # 步驟5. 持續的拉取Kafka有進來的訊息
    try:
        while True:
            # 請求Kafka把新的訊息吐出來
            records = consumer.consume(num_messages=500, timeout=1.0)  # 批次讀取
            if records is None:
                continue

            for record in records:
                # 檢查是否有錯誤
                if record is None:
                    continue
                if record.error():
                    # Error or event
                    if record.error().code() == KafkaError._PARTITION_EOF:
                        print('')
                        # End of partition event
                        # sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                        #                 (record.topic(), record.partition(), record.offset()))
                    else:
                        # Error
                        raise KafkaException(record.error())
                else:
                    # ** 在這裡進行商業邏輯與訊息處理 **
                    # 取出相關的metadata
                    topic = record.topic()
                    partition = record.partition()
                    offset = record.offset()
                    timestamp = record.timestamp()
                    # 取出msgKey與msgValue
                    msgKey = try_decode_utf8(record.key())
                    msgValue = try_decode_utf8(record.value())

                    if msgKey != 'end':
                        msgValue2 = msgValue.split(' ')
                        message = ''

                        for i in range(len(msgValue2)):
                            sql = '''select unitprice from product where productName = '{}';'''.format(msgValue2[i])
                            cursor.execute(sql)
                            data = cursor.fetchall()[0][0]
                            message += '{}:{}:{}:{}'.format(msgValue2[i], data, 1, data * 1)
                            if i < len(msgValue2) - 1:
                                message += ','

                        redis.set(msgKey, message)
                        with open('trade_user.txt','w',encoding='utf-8') as f:
                            f.write(msgKey)
                    else:
                        with open('trade_user.txt','r',encoding='utf-8') as f:
                            userID = f.read()
                        timestamp = timestamp[1]/1000
                        timestamp = time.localtime(timestamp)
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", timestamp)

                        trade_info = redis.get('{}'.format(ID))
                        for i in trade_info:
                            sql = '''select productID from product where productName = '{}';'''.format(i.split(':')[0])
                            cursor.execute(sql)
                            productID = cursor.fetchall()[0][0]
                            sql2 = '''INSERT INTO shoppinglist (userID,shoppingdate,productID,quantity) VALUE ('{}','{}','{}',1);'''.format(userID, timestamp, productID)
                            cursor.execute(sql2)
                            conn.commit()
                        url = 'http://localhost:5000/thank/{}'.format(userID)
                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
                        res = requests.get(url=url, headers=headers)

                    # 秀出metadata與msgKey & msgValue訊息
                    print('%s-%d-%d : (%s , %s)' % (topic, partition, offset, msgKey, msgValue))
                    print(timestamp)
    except KeyboardInterrupt as e:
        sys.stderr.write('Aborted by user\n')
    except Exception as e:
        sys.stderr.write(e)

    finally:
        # 步驟6.關掉Consumer實例的連線
        consumer.close()
        cursor.close()
        conn.close()