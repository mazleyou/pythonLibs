import requests
import pymysql
from apscheduler.schedulers.background import BackgroundScheduler
import time

import datetime


def klines():
    try:
        print("main start")
        conn = pymysql.connect(host='20.41.74.191', port=3306, user='root', passwd='taiholab', db='taiholab', charset='utf8', autocommit=True)
        curs = conn.cursor()

        market = 'BTCUSDT'
        tick_interval = '3m'

        url = 'https://api.binance.com/api/v1/klines?symbol=' + market + '&interval=' + tick_interval
        data = requests.get(url).json()

        dt = datetime.date.today().strftime("%Y%m%d")

        for row in data:
            curs.execute("""select * from BTCUSDT_KLINES where date = %s and OPEN_TIME = %s""", (dt, row[0]))
            exist_record = curs.fetchone()
            if exist_record is None:
                print(row[0])
                curs.execute("""insert into BTCUSDT_KLINES(DATE, OPEN_TIME, OPEN, HIGH, LOW, CLOSE, VOLUME, QUOTE, TRADES) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (dt, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    except Exception as e:
        print(e)

try:
    print("job start")
    sched = BackgroundScheduler()
    sched.start()
    sched.add_job(klines, 'interval', hours=4)
    # sched.add_job(main, 'interval', seconds=10)
except Exception as e:
    print(e)
while True:
    time.sleep(1000)