import pandas as pd
from datetime import datetime

time = datetime.today().strftime("%Y%m%d") + '160000'

code = '105840'

url = f'https://finance.naver.com/item/sise_time.nhn?code={code}&thistime={time}&page=1'
temp = pd.read_html(url)[0]
temp = temp.loc[temp["체결시각"].isnull() == False]
temp['체결가'] = temp['체결가'].astype(int)
temp['매도'] = temp['매도'].astype(int)
temp['매수'] = temp['매수'].astype(int)
temp['전일비'] = temp['전일비'].astype(int)
temp['거래량'] = temp['거래량'].astype(int)
temp['변동량'] = temp['변동량'].astype(int)
print(temp['체결가'])

