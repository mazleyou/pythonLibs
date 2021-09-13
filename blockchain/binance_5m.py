import requests
import pymysql

try:
    print("main start")
    conn = pymysql.connect(host='20.41.74.191', port=3306, user='root', passwd='taiholab', db='taiholab', charset='utf8', autocommit=True)
    curs = conn.cursor()

    markets = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT']
    tick_interval = '5m'

    for market in markets:
        url = 'https://api.binance.com/api/v1/klines?symbol=' + market + '&interval=' + tick_interval
        data = requests.get(url).json()

        select_query = "select * from " + market + "_KLINES_5M where OPEN_TIME = %s"
        insert_query = "insert into " + market + "_KLINES_5M(OPEN_TIME, OPEN, HIGH, LOW, CLOSE, VOLUME, TRADES) values (%s, %s, %s, %s, %s, %s, %s)"

        for row in data:
            open_time = int(str(row[0])[2:8])

            curs.execute(select_query, open_time)
            exist_record = curs.fetchall()

            # new kline
            if len(exist_record) == 0:
                curs.execute(insert_query, (open_time, row[1], row[2], row[3], row[4], row[5], row[7]))
                print(market)

except Exception as e:
    print(e)
