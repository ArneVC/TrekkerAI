import os
import requests
from urllib.parse import urlparse
import json
import time

json_file_path = "brand_images.json"

max_number_of_failed_download_retries = 5


def download_image(url, folder):
    retries = 0
    while retries < max_number_of_failed_download_retries:
        try:
            response = requests.get(url)
            response.raise_for_status()

            filename = os.path.join(folder, os.path.basename(urlparse(url).path))

            with open(filename, "wb") as file:
                file.write(response.content)

            print(f"Downloaded: {filename}")
            return
        except Exception as e:
            print(f"Failed to download {url}: {str(e)}")
            retries += 1
            if retries < max_number_of_failed_download_retries:
                print(
                    f"Retrying in 5 seconds... (Retry {retries}/{max_number_of_failed_download_retries})"
                )
                time.sleep(5)
            else:
                print(f"Maximum retries reached for {url}")


with open(json_file_path, "r") as json_file:
    json_data = json.load(json_file)

for entry in json_data:
    brand = entry["brand"]
    image_urls = entry["images"]

    if not os.path.exists(brand):
        os.makedirs(brand)

    for image_url in image_urls:
        download_image(image_url, brand)
