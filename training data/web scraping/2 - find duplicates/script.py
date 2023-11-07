import json

with open("brands.json", "r") as json_file:
    data = json.load(json_file)

brand_link_dict = {}

for entry in data:
    brand_link = entry["BrandLink"]
    label = entry["Label"]

    if brand_link in brand_link_dict:
        brand_link_dict[brand_link].append(label)
    else:
        brand_link_dict[brand_link] = [label]

for brand_link, labels in brand_link_dict.items():
    if len(labels) > 1:
        print(f"Entries with the same BrandLink ({brand_link}): {', '.join(labels)}")
