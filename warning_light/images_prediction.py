from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid
import images_augmentation
import cv2

# Replace with valid values
ENDPOINT = "https://westeurope.api.cognitive.microsoft.com/"
training_key = "7498737fe11240d5b558a6e5001450fe"
prediction_key = "7498737fe11240d5b558a6e5001450fe"

publish_iteration_name = "Iteration1"

# Now there is a trained endpoint that can be used to make a prediction
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)

# Create a new project
print("Creating project...")
project_name = uuid.uuid4()
project = trainer.get_projects()

base_image_location = os.path.join(os.path.dirname(__file__), "test_images")
file_list = os.listdir(base_image_location)
for file in file_list:
    filename = file.split(".", 1)
    if len(filename) > 1 and 'png' in filename[1]:
        # Use prediction model
        with open(os.path.join(base_image_location, file), "rb") as image_contents:
            results = predictor.classify_image(
                project[0].id, publish_iteration_name, image_contents.read())

            # Display the results.
            for prediction in results.predictions:
                if prediction.probability > 0.5:
                    print(file + "\t" + prediction.tag_name +
                          ": {0:.2f}%".format(prediction.probability * 100))