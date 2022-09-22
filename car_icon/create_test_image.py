import os
import images_augmentation
import cv2

# get source image file list
base_image_location = os.path.join(os.path.dirname(__file__), "Images")
file_list = os.listdir(base_image_location)
for file in file_list:
    if '.' in file:
        img = cv2.imread('./Images/' + file)
        augmented_images = images_augmentation.get_image([img])

        filename = file.split(".", 1)

        for img in augmented_images:
            cv2.imwrite('./test_images/' + filename[0] + '.png', img)
