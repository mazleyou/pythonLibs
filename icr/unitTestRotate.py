import json

from PIL import Image
import math
import os
from appODBC import msOcrCall, findDocType, labelLineSearch, findCellPhoneReceiptDate, findSingleField, \
    findCellPhoneReceiptAmt
from utils.ocrjson_rotate import get_rotated_json


def rotate(x, y, theta, pi=3.14):
    radian = theta * pi / 180
    sin = math.sin(radian)
    cos = math.cos(radian)
    new_x = cos*x - sin*y
    new_y = sin*x + cos*y
    return new_x, new_y


def rotate_img(ori, theta):
    dst = Image.new("RGB", ori.size, (0, 0, 0))
    width, height = ori.size
    pixels_dst = dst.load()
    pixels_ori = ori.load()
    for y in range(height):
        for x in range(width):
            rotate_x, rotate_y = rotate(x, y, theta)
            if 0 <= rotate_x < width and 0 <= rotate_y < height:
                pixels_dst[rotate_x, rotate_y] = pixels_ori[x, y]
    return dst

def get_sample_ocr():
    ret = '[{"location": "956,224,324,42", "text": "SAMSUNG 삼성전자서비스"}, {"location": "611,322,388,65", "text": "수 리 비 명 세 서"}, {"location": "552,570,174,30", "text": "2020 408: 22"}, {"location": "899,559,412,36", "text": "사면식 표기로 수비시 화들어 서생및 2%) 는"}, {"location": "377,614,94,26", "text": "합계금액"}, {"location": "585,625,113,30", "text": "-254.000"}, {"location": "865,625,-16,18", "text": "R"}, {"location": "370,642,99,22", "text": "VATT PA"}, {"location": "289,729,376,27", "text": "ElLISM-NOSON 冷상 교수 가 로 수라"}, {"location": "1088,733,72,25", "text": "18.182"}, {"location": "1198,737,64,24", "text": "1:818"}, {"location": "1064,775,95,31", "text": "212,728"}, {"location": "1194,778,70,29", "text": "21.272"}, {"location": "304,939,234,24", "text": "FO RUE PFINOSON"}, {"location": "938,919,17,24", "text": "1"}, {"location": "1077,918,90,27", "text": "177.273"}, {"location": "1193,915,78,32", "text": "17.727"}, {"location": "306,969,427,23", "text": "GH97-21089RUMEA BACK GLASS-KOŃ_201"}, {"location": "1088,968,79,21", "text": "35.455"}, {"location": "1102,1549,97,25", "text": "230.919"}, {"location": "1227,1545,85,28", "text": "29.090"}, {"location": "317,1618,218,31", "text": "- @w:GM-NBsOF"}, {"location": "424,1618,-122,-23", "text": "古世验区 画"}, {"location": "982,1616,287,36", "text": "44900 : A0002776100"}, {"location": "313,1653,554,28", "text": "목양한급 및 서비스대용을 협의 카대 명세 합니다."}, {"location": "1063,1821,408,39", "text": "고한번대처전비 자보 호 2-06-9218 37:10"}]'
    return json.loads(ret)

if __name__ == '__main__':
    try:
        # fileName = "../sample/1.jpg"
        # fileName = "D:/hskim/workspace/node/ICR-CARROT-WEB/uploads/2.png"
        path_dir = "../sample"
        file_list = os.listdir(path_dir)

        for file_name in file_list:
            data = msOcrCall(path_dir + '/' + file_name)
            retOcr = get_rotated_json(data, path_dir + '/' + file_name)
            # retOcr = get_sample_ocr()
            print(retOcr)
            docTopType, docType, maxNum = findDocType(retOcr)

            retOcr, labellist = labelLineSearch(retOcr, docTopType)

            retOcr = findSingleField(docTopType, docType, 'horizon', retOcr, labellist)

            print(retOcr)

    except Exception as e:
        print(e)