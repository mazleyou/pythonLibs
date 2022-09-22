from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

# Replace with valid values
ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com/"
training_key = "10fe1b51389742bb84e20b20950d6901"
prediction_key = "PASTE_YOUR_CUSTOM_VISION_PREDICTION_SUBSCRIPTION_KEY_HERE"
prediction_resource_id = "PASTE_YOUR_CUSTOM_VISION_PREDICTION_RESOURCE_ID_HERE"

publish_iteration_name = "classifyModel"


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]


credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)

# Create a new project
print("Creating project...")
project_name = uuid.uuid4()
project = trainer.get_projects()

tags = trainer.get_tags(project[0].id)
base_image_location = os.path.join(os.path.dirname(__file__), "Images")

print("Adding images...")

image_list = []

for tag in tags:
    for image_num in range(0, 4):
        file_name = tag.name + "_" + str(image_num) + '.png'
        with open(os.path.join(base_image_location, tag.name, file_name), "rb") as image_contents:
            print(image_contents)
            image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[tag.id]))

list_chunked = list_chunk(image_list, 63)

for chunk in list_chunked:
    upload_result = trainer.create_images_from_files(project[0].id, ImageFileCreateBatch(images=chunk))

    if not upload_result.is_batch_successful:
        print("Image batch upload failed.")
        for image in upload_result.images:
            print("Image status: ", image.status)
        exit(-1)

#     with open(os.path.join(base_image_location, "Hemlock", file_name), "rb") as image_contents:
#
#
# for image_num in range(1, 11):
#     file_name = "japanese_cherry_{}.jpg".format(image_num)
#     with open(os.path.join(base_image_location, "Japanese_Cherry", file_name), "rb") as image_contents:
#         image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[cherry_tag.id]))
#
# upload_result = trainer.create_images_from_files(project.id, ImageFileCreateBatch(images=image_list))
# if not upload_result.is_batch_successful:
#     print("Image batch upload failed.")
#     for image in upload_result.images:
#         print("Image status: ", image.status)
#     exit(-1)