import json
import requests
from bs4 import BeautifulSoup

brand_tractors = {}

with open("brands_filtered_manually.json", "r") as file:
    data = json.load(file)

for entry in data:
    label = entry["Label"]
    link = entry["BrandLink"]
    tractors = []

    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        td_menu_element = soup.find(class_="tdMenu1")

        if not td_menu_element:
            td_menu_element = soup.find(class_="tdmenu1")

        if td_menu_element:
            tbody_element = td_menu_element.find("tbody")

            if tbody_element:
                tr_elements = tbody_element.find_all("tr")

                for i in range(1, len(tr_elements)):
                    tr = tr_elements[i]
                    td_elements = tr.find_all("td")

                    if len(td_elements) >= 3:
                        third_td_text = td_elements[2].get_text()
                        first_4_chars = third_td_text[:4]

                        if first_4_chars != "unkn" and (
                            not first_4_chars.isdigit() or int(first_4_chars) >= 1980
                        ):
                            a_tag = td_elements[0].find("a")
                            if a_tag and a_tag.get("href"):
                                href_value = a_tag.get("href")
                                tractors.append(href_value)
                                print(
                                    f"Found eligible tractor for {label}: {href_value}"
                                )

            else:
                print(
                    f"Label: {label}, Link: {link}, No tbody element found in tdMenu1 class."
                )
        else:
            print(f"Label: {label}, Link: {link}, No element with class tdMenu1 found.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to visit: {label}, Link: {link}, Error: {e}")
    brand_tractors[label] = tractors

brand_images = {}

minimum_tractors_threshold = 20

for brand, tractors in brand_tractors.items():
    if len(tractors) >= minimum_tractors_threshold:
        brand_images[brand] = []

        for tractor_link in tractors:
            try:
                response = requests.get(tractor_link)
                response.raise_for_status()
                tractor_soup = BeautifulSoup(response.text, "html.parser")
                img_elements = tractor_soup.find_all("img")
                if len(img_elements) >= 2:
                    second_img_src = img_elements[1].get("src")
                    brand_images[brand].append(second_img_src)
                    print(f"got image link: {second_img_src}")

            except requests.exceptions.RequestException as e:
                print(
                    f"Failed to visit tractor link for {brand}: {tractor_link}, Error: {e}"
                )

print("filtering images")

for brand, images in brand_images.items():
    filtered_images = [
        image
        for image in images
        if image != "https://www.tractordata.com/photos/none-td3a.jpg"
    ]
    brand_images[brand] = filtered_images

output_data = []
for brand, images in brand_images.items():
    output_data.append({"brand": brand, "images": images})

with open("brand_images.json", "w") as output_file:
    json.dump(output_data, output_file, indent=4)
