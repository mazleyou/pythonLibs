from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

# Replace with valid values
ENDPOINT = "https://westeurope.api.cognitive.microsoft.com/"
training_key = "7498737fe11240d5b558a6e5001450fe"
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

print("Training...")
iteration = trainer.train_project(project[0].id)

while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project[0].id, iteration.id)
    print ("Training status: " + iteration.status)
    print ("Waiting 10 seconds...")
    time.sleep(10)