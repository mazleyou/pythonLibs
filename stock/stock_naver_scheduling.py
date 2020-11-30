from apscheduler.schedulers.background import BackgroundScheduler
import time
import pandas as pd
import datetime
import pymysql
import random

THRESHOLD = 1.012
INDEX_TIME = [datetime.time(9, 0), datetime.time(9, 30), datetime.time(10, 0), datetime.time(10, 30), datetime.time(11, 0), datetime.time(11, 30),datetime.time(12, 0), datetime.time(12, 30), datetime.time(13, 0), datetime.time(13, 30), datetime.time(14, 0), datetime.time(14, 30), datetime.time(15, 0), datetime.time(15, 30), datetime.time(16, 0)]
insert_sql = """insert into sise_time(DATE,CODE,TIME,PRICE,SELLING,BUYING,VOLUME) values (%s, %s, %s, %s, %s, %s, %s)"""
INSERT_UP = """insert into sise_up(DATE,CODE,TIME) values (%s, %s, %s)"""
delaytime = random.uniform(2, 4) / 2

def ret_flag(lastprice, nowprice):
    retnum = 5
    if lastprice * THRESHOLD <= nowprice:
        retnum = 6
    elif lastprice >= nowprice * THRESHOLD:
        retnum = 4
    return retnum

def getStock(code):
    try:
        print(code)
        dt = datetime.date.today().strftime("%Y%m%d")
        conn = pymysql.connect(host='20.41.74.191', port=3306, user='root', passwd='taiholab', db='taiholab',
                               charset='utf8', autocommit=True)
        curs = conn.cursor()
        searchtime = dt + '160000'
        dict_temp = {}
        for page in range(1, 43):
            url = f'https://finance.naver.com/item/sise_time.nhn?code={code}&thistime={searchtime}&page={page}'
            temp = pd.read_html(url)[0]
            temp = temp.loc[temp["체결시각"].isnull() == False]
            temp['체결가'] = temp['체결가'].astype(int)
            temp['매도'] = temp['매도'].astype(int)
            temp['매수'] = temp['매수'].astype(int)
            temp['전일비'] = temp['전일비'].astype(int)
            temp['거래량'] = temp['거래량'].astype(int)
            temp['변동량'] = temp['변동량'].astype(int)

            for i, row in temp.iterrows():
                # curs.execute(insert_sql, (dt, code, row["체결시각"], row['체결가'], row['매도'], row['매수'], row['거래량']))
                dict_temp[datetime.time(int(row["체결시각"].split(":")[0]), int(row["체결시각"].split(":")[1]))] = row['체결가']
            # time.sleep(round(delaytime, 1))

        indexprice = 0

        for n, time in enumerate(INDEX_TIME):
            timelist = list(dict_temp.keys())
            # 내림차순의 시간 리스트
            sortedtime = sorted(timelist)

            for m, gettime in enumerate(sortedtime):
                if gettime >= time:
                    if n != 0:
                        if (ret_flag(indexprice, dict_temp[gettime]) == 6):
                            curs.execute(INSERT_UP, (dt, code, str(n)))
                    indexprice = dict_temp[gettime]
                    break

        conn.close()
    except Exception as e:
        print(e)

def priceCheck(str):
    try:
        retval = 0
        if len(str) > 0:
            str = str.replace(",", "")
            retval = int(str)
        return retval
    except ValueError as e:
        print(e)
        return 0

def crawling_job():
    stock_xlsx = pd.read_excel('data.xls', dtype={'종목코드': str, '기업명': str, '자본금(원)': str})
    # 'DataFrame.loc' 이용해서 사용할 컬럼만 추출
    stock_df = stock_xlsx.loc[:, ['종목코드', '기업명', '자본금(원)']]

    for i, row in stock_df.iterrows():
        # 엑셀 리스트중 자본금 하한 체크
        if priceCheck(row['자본금(원)']) > 30000000000:
            getStock(row['종목코드'])

def count_job():
    conn = pymysql.connect(host='20.41.74.191', port=3306, user='root', passwd='taiholab', db='taiholab',
                           charset='utf8', autocommit=True)
    curs = conn.cursor(pymysql.cursors.DictCursor)

    curs.execute("""select max(date) as maxdate from sise_up""")
    maxdate = curs.fetchone()

    curs.execute("""select * from sise_up where date = %s""", maxdate['maxdate'])
    rows = curs.fetchall()
    conn.close()

    for index_time in range(1, 12):
        now_codes = list(row['CODE'] for row in rows if row['TIME'] == index_time)
        next_codes = list(row['CODE'] for row in rows if row['TIME'] == index_time + 1)
        for nowcode in now_codes:
            for nextcode in next_codes:
                codes = nowcode + nextcode
                conn = pymysql.connect(host='20.41.74.191', port=3306, user='root', passwd='taiholab', db='taiholab',
                                       charset='utf8', autocommit=True)
                curs = conn.cursor(pymysql.cursors.DictCursor)
                curs.execute("""select count from sise_count where codes = %s""", codes)
                count = curs.fetchone()
                if count is None:
                    curs.execute("""insert into sise_count(CODES) values (%s)""", codes)
                else:
                    curs.execute("""update sise_count set count=%s where codes=%s""", (str(count['count'] + 1), codes))
                conn.close()


try:
    print("job start")
    sched = BackgroundScheduler()
    sched.start()
    # 0-4 weekday
    sched.add_job(crawling_job, 'cron', day_of_week='0-4', hour=17,  minute=30)
    sched.add_count(count_job, 'cron', day_of_week='0-4', hour=6,  minute=30)
except Exception as e:
    print(e)
while True:
    time.sleep(1000)
