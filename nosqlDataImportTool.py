# Simple script to combine multiple JSON documents for importation into MongoDb
# Note that NoSQL and MongoDb treat the files independently - script is just for importation purposes 

import os, json

input_dir = "/mnt/c/Users/jfrin/Documents/projects/AI/VERA/data"
output_file = "/mnt/c/Users/jfrin/Documents/projects/AI/VERA/data/veraDocs.json"
docs = []
for filename in sorted(os.listdir(input_dir)):
    if filename.endswith(".json"):
        with open(os.path.join(input_dir, filename), "r") as f:
            docs.append(json.load(f))

with open(output_file, "w") as f:
    json.dump(docs, f, indent=2)