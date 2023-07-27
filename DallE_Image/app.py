from flask import Flask, request, render_template
from azure.storage.blob import BlobServiceClient
import requests
import os
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_image', methods=['POST'])
def generate_image():
    # Get Azure OpenAI Service settings
    api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = '2023-06-01-preview'

    # Get user input from form
    prompt = request.form['prompt']

    # Make the initial call to start the job
    url = "{}openai/images/generations:submit?api-version={}".format(api_base, api_version)
    headers= { "api-key": api_key, "Content-Type": "application/json" }
    body = {
        "prompt": prompt,
        "n": 1,
        "size": "512x512"
    }
    submission = requests.post(url, headers=headers, json=body)

    # Get the operation-location URL for the callback
    operation_location = submission.headers['Operation-Location']

    # Poll the callback URL until the job has succeeeded
    status = ""
    while (status != "succeeded"):
        time.sleep(3)
        response = requests.get(operation_location, headers=headers)
        status = response.json()['status']

    # Get the URL of the generated image
    image_url = response.json()['data'][0]['url']

    # Save the image to Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
    container_name = "images"
    blob_name = "{}.png".format(int(time.time()))
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    image_data = requests.get(image_url).content
    blob_client.upload_blob(image_data)

    # Return the image URL to the user
    return render_template('image.html', image_url=blob_client.url)

if __name__ == '__main__':
    app.run()