from PIL import ImageFont, ImageDraw, Image


def json_to_image(file_name, data, angle):
    im = Image.open(file_name)

    rotated = im.rotate(angle)
    rotated = rotated.convert('RGB')

    # rotated.show()
    fontpath = "fonts/gulim.ttc"
    font = ImageFont.truetype(fontpath, 80)
    draw = ImageDraw.Draw(rotated)
    for item in data:
        locations = item['location'].split(',')

        x1, y1 = int(locations[0]), int(locations[1])
        x2, y2 = int(locations[0]) + int(locations[2]), int(locations[1]) + int(locations[3])

        draw.rectangle(((x1, y1), (x2, y2)), outline=(0, 0, 255), width=4)
        draw.text((x1, y1), item['text'], font=font, fill=(255, 0, 0, 0))

    # rotated.show()
    return rotated