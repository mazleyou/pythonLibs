import os
import images_augmentation
import cv2

isExist = os.path.exists('./test_images')
if not isExist:
    os.makedirs('./test_images')

# get source image file list
base_image_location = os.path.join(os.path.dirname(__file__), "Images")
file_list = os.listdir(base_image_location)
for file in file_list:
    filename = file.split(".", 1)
    if len(filename) > 1 and 'png' in filename[1]:
        img = cv2.imread('./Images/' + file)
        augmented_images = images_augmentation.get_image([img])

        for img in augmented_images:
            cv2.imwrite('./test_images/' + file, img)
