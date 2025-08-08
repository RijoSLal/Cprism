import requests
import cv2 

url = "http://ec2-51-21-252-101.eu-north-1.compute.amazonaws.com:8000/upload"
image_path = "test_images/tmp9y3n4mx4.png"

with open(image_path, "rb") as f:
    files = {
        'file': (image_path, f, 'image/png')  
    }

    response = requests.post(url, files=files)

if response.status_code==200:
    output = response.json()
    print([(k,len(v)) for k,v in output["Prediction"].items()])


else:
    print("some error occured")