import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2

import pandas as pd
from moviepy.editor import VideoFileClip

def get_offset_for_true_mm(text, draw, font):
    anchor_bbox = draw.textbbox((0, 0), text, font=font, anchor='lt')
    anchor_center = (anchor_bbox[0] + anchor_bbox[2]) // 2, (anchor_bbox[1] + anchor_bbox[3]) // 2
    mask_bbox = font.getmask(text).getbbox()
    mask_center = (mask_bbox[0] + mask_bbox[2]) // 2, (mask_bbox[1] + mask_bbox[3]) // 2
    return anchor_center[0] - mask_center[0], anchor_center[1] - mask_center[1]

def pipeline(frame):
    try:
        # cv2 -> PIL 이미지로 변경
        color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(color_coverted)
        font = ImageFont.truetype("./malgun.ttf", 48)
        # PIL 이미지에 한글 입력
        draw = ImageDraw.Draw(img_pil)
        text = "the parametric pattern of the wind cascading Grill shine three-dimensionally"
        offset = get_offset_for_true_mm(text, draw, font)

        draw.text((50 + offset[0], 800 + offset[1]), text, font=font, fill=(255, 255, 255))

        text = "this parametric surfaces and both new asset lines create a feeling of tension."
        offset = get_offset_for_true_mm(text, draw, font)

        draw.text((50 + offset[0], 850 + offset[1]), text, font=font, fill=(255, 255, 255))

        text = "바람 계단식 그릴의 파라 메트릭 패턴은"
        offset = get_offset_for_true_mm(text, draw, font)

        draw.text((50 + offset[0], 900 + offset[1]), text, font=font, fill=(255, 255, 255))

        text = "3 차원으로 빛나는이 파라 메트릭 표면과 새로운 자산 라인이 긴장감을 만듭니다."
        offset = get_offset_for_true_mm(text, draw, font)

        draw.text((50 + offset[0], 950 + offset[1]), text, font=font, fill=(255, 255, 255))
        # PIL 이미지 -> cv2 Mat 타입으로 변경
        numpy_img = np.array(img_pil)
        frame = cv2.cvtColor(numpy_img, cv2.COLOR_RGB2BGR)

        # cv2.putText(frame,
        #             'the parametric pattern of the wind cascading Grill shine three-dimensionally',
        #             (10, 50),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA, True)
        # cv2.putText(frame,
        #             'this parametric surfaces and both new asset lines create a feeling of tension.',
        #             (10, 150),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA, True)
        # cv2.putText(frame, '바람 계단식 그릴의 파라 메트릭 패턴은',
        #             (10, 250),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA, True)
        # cv2.putText(frame, '3 차원으로 빛나는이 파라 메트릭 표면과 새로운 자산 라인이 긴장감을 만듭니다.',
        #             (10, 350),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3, cv2.LINE_AA, True)
    except StopIteration:
        pass
    # additional frame manipulation
    return frame

# dfi = pd.read_csv('data.csv').iterrows()
video = VideoFileClip("avante_en.mp4")
out_video = video.fl_image(pipeline)
out_video.write_videofile("vidout.mp4", audio=False)