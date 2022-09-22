import os
import cv2
import numpy as np
import imgaug.augmenters as iaa
import images_augmentation
# get image file list
base_image_location = os.path.join(os.path.dirname(__file__), "Images")
file_list = os.listdir(base_image_location)
for file in file_list:
    if '.' in file:
        img = cv2.imread('./Images/' + file)

        images = [img]

        for batch_idx in range(4):
            # image create from augmentation
            augmented_images = images_augmentation.get_image(images)

            filename = file.split(".", 1)
            isExist = os.path.exists('./Images/' + filename[0])
            if not isExist:
                os.makedirs('./Images/' + filename[0])

            # image save
            for img in augmented_images:
                cv2.imwrite('./Images/' + filename[0] + '/' + filename[0] + '_' + str(batch_idx) + '.png', img)






