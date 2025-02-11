# 详细教程参考 https://microsoftlearning.github.io/mslearn-ai-vision/Instructions/Exercises/01-analyze-images.html

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import json
import os

client = ImageAnalysisClient(
    endpoint=os.environ["VISION_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["VISION_KEY"])
)

imagePath = './Copilot/img/copilot-cli-auth.png'
imageData = open(imagePath, "rb")
# print(imageData)
# exit()
outputLanguage = 'en'
result = client.analyze(
    image_data = imageData,
    visual_features=[VisualFeatures.CAPTION, VisualFeatures.READ],
    gender_neutral_caption=True,
    language=outputLanguage,
)
print(result)
