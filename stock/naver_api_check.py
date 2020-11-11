import pandas as pd
from datetime import datetime
from datetime import time
import numpy
THRESHOLD = 1.02
INDEX_TIME = [time(9, 0), time(9, 30), time(10, 0), time(10, 30), time(11, 0), time(11, 30), time(12, 0), time(12, 30), time(13, 0), time(13, 30), time(14, 0), time(14, 30), time(15, 0), time(15, 30), time(16, 0)]

def ret_flag(lastprice, nowprice):
    retnum = 5
    if lastprice * THRESHOLD <= nowprice:
        retnum = 6
    elif lastprice >= nowprice * THRESHOLD:
        retnum = 4
    return retnum

today = datetime.today().strftime("%Y%m%d") + '160000'


# all_list = []
code = '105840'
dict_temp = {}
# for page in range(1, 43):
for page in range(1, 43):
    url = f'https://finance.naver.com/item/sise_time.nhn?code={code}&thistime={today}&page={page}'
    temp = pd.read_html(url)[0]
    temp = temp.loc[temp["체결시각"].isnull() == False]
    temp['체결가'] = temp['체결가'].astype(int)
    temp['매도'] = temp['매도'].astype(int)
    temp['매수'] = temp['매수'].astype(int)
    temp['전일비'] = temp['전일비'].astype(int)
    temp['거래량'] = temp['거래량'].astype(int)
    temp['변동량'] = temp['변동량'].astype(int)

    for i, row in temp.iterrows():
        dict_temp[time(int(row["체결시각"].split(":")[0]), int(row["체결시각"].split(":")[1]))] = row['체결가']
    # all_list.extend(temp.values.tolist())
# print(all_list)
# b = pd.DataFrame(all_list)[0]
# print(b.to_list())
# map_list = map(time, all_list[0])
indexprice = 0

for n, time in enumerate(INDEX_TIME):
    timelist = list(dict_temp.keys())
    # 내림차순의 시간 리스트
    sortedtime = sorted(timelist)

    for m, gettime in enumerate(sortedtime):
        if gettime >= time:
            if n != 0:
                d = gettime.strftime("%H:%M")
                print(ret_flag(indexprice, dict_temp[gettime]))

            indexprice = dict_temp[gettime]
            break
print(indexprice)


