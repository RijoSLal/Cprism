import requests


url = "http://ec2-51-21-252-101.eu-north-1.compute.amazonaws.com:8000/upload"

with open("test_images/tmp9y3n4mx4.png","r") as file:
    img_file = file.read()

files = {'image': ('image.jpg', img_file, 'image/jpeg')}

response = requests.post(url=url,files=files)

if response.status_code == 200:
    print("Image uploaded successfully!")
    print(response.json()) 
else:
    print(f"Image upload failed with status code: {response.status_code}")
    print(response.text)