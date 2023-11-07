import requests
from lxml import html
import json

# inputs
url = "https://www.tractordata.com/farm-tractors/"


# class
class BrandEntry:
    def __init__(self, label, brandLink):
        self.brandLink = brandLink
        self.label = label

    def toString(self):
        return "BRANDNAME: " + self.label + "\n" + "LINK: " + self.brandLink

    def to_dict(self):
        return {"Label": self.label, "BrandLink": self.brandLink}


html_content = ""
try:
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve the web page. Status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

parsed_html = html.fromstring(html_content)
table_elements = parsed_html.xpath('//table[@class="tdMenu1"]')

brands = []
if table_elements:
    for row in table_elements[0].xpath(".//tr"):
        link = row.xpath(".//td[1]//a/@href")
        text = row.xpath(".//td[1]//a/text()")
        if link:
            brand = BrandEntry(text[0], link[0])
            brands.append(brand)
else:
    print("Table with the specified class not found")

json_file = "brands.json"
with open(json_file, "w") as file:
    data = [brand.to_dict() for brand in brands]
    json.dump(data, file, indent=2)

print(f"Data written to {json_file}")
