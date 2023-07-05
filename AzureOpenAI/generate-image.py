import requests
import time
import os
from dotenv import load_dotenv

def main(): 
        
    try:
        # Get Azure OpenAI Service settings
        api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")

        api_version = '2023-06-01-preview'
        
        # Get prompt for image to be generated
        prompt = input("Enter a prompt to request an image: ")

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

        # Get the results
        image_url = response.json()['result']['data'][0]['url']

        # Display the URL for the generated image
        print(image_url)
        # save the image to a file, file name is current date time .png.
        image = requests.get(image_url)
        image_save_name = time.strftime("%Y%m%d-%H%M%S") + '.png'
        with open(image_save_name, 'wb') as f:
            f.write(image.content)

    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()
# 如果长时间没有反应，可以能是触发了Azure OpenAI敏感信息的限制，可以在Azure Portal中再测试验证。

