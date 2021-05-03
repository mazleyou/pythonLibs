from utils.json_to_image import json_to_image
import math


def get_new_location(origin_x, origin_y, angle, width, height):
    rad = math.pi * angle / 180.0
    # 이미지 기준 좌표를 원점 기준 좌표로 전환
    if -135 < angle <= -45:
        origin_x = origin_x - width
        origin_y = height - origin_y
    elif -225 < angle <= -135:
        origin_x = origin_x - width
        origin_y = -height + origin_y - height
    elif 45 < angle <= 135:
        origin_y = - origin_y
    else:
        origin_y = height - origin_y

    new_x = int(origin_x * math.cos(rad) - origin_y * math.sin(rad))
    new_y = int(origin_x * math.sin(rad) + origin_y * math.cos(rad))

    # 원점 기준 좌표를 이미지 기준 좌표로 전환
    if -135 < angle <= -45:
        new_y = int(-width * math.sin(rad)) - new_y
    elif -225 < angle <= -135:
        new_y = new_y - int(-height * math.cos(rad))
    elif 45 < angle <= 135:
        new_y = int(width * math.sin(rad)) - new_y
    else:
        new_y = int(height * math.cos(rad)) - new_y
    return new_x, new_y


def get_rotated_json(body, file_name):
    data = []
    angle = body['analyzeResult']['readResults'][0]['angle']
    width = body['analyzeResult']['readResults'][0]['width']
    height = body['analyzeResult']['readResults'][0]['height']

    for i in body['analyzeResult']['readResults'][0]['lines']:
        new_start_x, new_start_y = get_new_location(i["boundingBox"][0], i["boundingBox"][1], angle, width, height)
        new_end_x, new_end_y = get_new_location(i["boundingBox"][4], i["boundingBox"][5], angle, width, height)
  
        location = str(new_start_x) + ',' + str(new_start_y) + ',' + str(new_end_x - new_start_x) + ',' + str(new_end_y - new_start_y)

        data.append({"location": location, "text": i['text'].replace("'", "").replace('"', '')})

    # json_to_image(file_name, data, angle).save(file_name + '_conv.png', "png")

    return data
