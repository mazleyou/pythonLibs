from xml.etree import ElementTree
import datetime
import requests

time = datetime.date.today().strftime("%Y%m%d") + '160000'

code = '105840'

url = f'http://asp1.krx.co.kr/servlet/krx.asp.XMLSiseEng?code={code}'
res = requests.get(url)
text = res.text[res.text.find('<?xml'):]
root_element = ElementTree.fromstring(text)
TBL_TimeConclude = root_element.iter(tag="TBL_TimeConclude")

for element in TBL_TimeConclude:
    for i in element:
        time = i.attrib['time']
        negoprice = i.attrib['negoprice']
        Dungrak = i.attrib['Dungrak']
        Debi = i.attrib['Debi']
        sellprice = i.attrib['sellprice']
        buyprice = i.attrib['buyprice']
        amount = i.attrib['amount']
        print(amount)
