import os
import cv2
import numpy as np
import imgaug.augmenters as iaa
import images_augmentation
# get image file list
base_image_location = os.path.join(os.path.dirname(__file__), "Images")
file_list = os.listdir(base_image_location)
for file in file_list:
    filename = file.split(".", 1)
    if '.' in filename[1]:
        filename = file.split(".", 1)[0]
        img = cv2.imread('./Images/' + file)

        images = [img]

        for batch_idx in range(4):
            # image create from augmentation
            augmented_images = images_augmentation.get_image(images)

            isExist = os.path.exists('./Images/' + filename)
            if not isExist:
                os.makedirs('./Images/' + filename)

            # image save
            for aug_img in augmented_images:
                cv2.imwrite('./Images/' + filename + '/' + filename + '_' + str(batch_idx) + '.png', aug_img)

        cv2.imwrite('./Images/' + filename + '/' + filename + '_4.png', img)







