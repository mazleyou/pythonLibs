from apscheduler.schedulers.background import BackgroundScheduler
import time
import pandas as pd
from datetime import datetime
import pymysql
from time import sleep
import random

def job():
    print("I'm working...", "| [time] ", str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min) + ":" + str(time.localtime().tm_sec))

    delaytime = random.uniform(2, 4)
    delaytime = delaytime / 2

    # stock_xlsx = pd.read_excel('/home/taihoinst/stockCrawling/stock.xls', dtype = {'종목코드': str, '기업명': str, '액면가(원)': str})
    stock_xlsx = pd.read_excel('stock.xls', dtype={'종목코드': str, '기업명': str, '자본금(원)': str})

    insert_sql = """insert into sise_time(DATE,CODE,TIME,PRICE,COMPARE,SELLING,BUYING,VOLUME,FLUCTUATION) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    insert_history_sql = """insert into sise_time_update_history(date, code, state) values(%s, %s, %s)"""
    update_history_sql = """update sise_time_update_history set state=%s where code=%s and date=%s"""
    sel_history_sql = """select * from sise_time_update_history where date = %s and code = %s"""
    del_sise_sql = """delete from sise_time where date = %s and code = %s"""

    def priceCheck(str):
        try:
            retval = 0
            if len(str) > 0:
                str = str.replace(",", "")
                retval = int(str)
            return retval
        except ValueError:
            return 0

    def getStock(code, dt):
        try:
            conn = pymysql.connect(host='20.41.74.191', port=3306, user='root', passwd='taiholab', db='taiholab',
                                   charset='utf8', autocommit=True)
            curs = conn.cursor()

            time = dt + '160000'
            for page in range(1, 43):
                url = f'https://finance.naver.com/item/sise_time.nhn?code={code}&thistime={time}&page={page}'
                temp = pd.read_html(url)[0]
                temp = temp.loc[temp["체결시각"].isnull() == False]
                temp['체결가'] = temp['체결가'].astype(int)
                temp['매도'] = temp['매도'].astype(int)
                temp['매수'] = temp['매수'].astype(int)
                temp['전일비'] = temp['전일비'].astype(int)
                temp['거래량'] = temp['거래량'].astype(int)
                temp['변동량'] = temp['변동량'].astype(int)

                for i, row in temp.iterrows():
                    curs.execute(insert_sql, (
                    dt, code, row["체결시각"], row['체결가'], row['전일비'], row['매도'], row['매수'], row['거래량'], row['변동량']))
                sleep(round(delaytime, 1))

            conn.close()
        except Exception as e:
            print(e)

    # 'DataFrame.loc' 이용해서 사용할 컬럼만 추출
    stock_df = stock_xlsx.loc[:, ['종목코드', '기업명', '자본금(원)']]

    conn = pymysql.connect(host='20.41.74.191', port=3306, user='root', passwd='taiholab', db='taiholab',
                           charset='utf8', autocommit=True)
    curs = conn.cursor()

    today_date = datetime.today().strftime("%Y%m%d")

    s = 0
    for i, row in stock_df.iterrows():
        # 엑셀 리스트중 자본금 하한 체크
        if priceCheck(row['자본금(원)']) > 30000000000:
            s = s + 1
            print(str(s) + ' : ' + str(priceCheck(row['자본금(원)'])) + ' : ' + row['종목코드'])
            # 히스토리 로그 테이블에 당일 기록이 있는지 확인
            curs.execute(sel_history_sql, (today_date, row['종목코드']))
            res = curs.fetchall()

            if len(res) == 0:
                curs.execute(insert_history_sql, (today_date, row['종목코드'], 'START'))
                getStock(row['종목코드'], today_date)
                curs.execute(update_history_sql, ('END', row['종목코드'], today_date))
            else:
                if res[0][3] == "START":
                    curs.execute(del_sise_sql, (today_date, row['종목코드']))
                    getStock(row['종목코드'], today_date)
                    curs.execute(update_history_sql, ('END', row['종목코드'], today_date))

    print('------------')

    conn.close()

sched = BackgroundScheduler()
sched.start()
# 0-4 weekday
sched.add_job(job, 'cron', day_of_week='0-4', hour=16,  minute=40)

while True:
    # print("Running main process...............")
    time.sleep(100)
