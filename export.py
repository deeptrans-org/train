import sys
import os
import re
from tqdm import tqdm
from pymongo import MongoClient, UpdateOne

# from languages import languages

client = MongoClient("mongodb://localhost:27017")
db = client["cp-250227"]

collections = db.list_collection_names()

if len(sys.argv) < 2:
    print("Usage: python export.py <name> <code> <code> ...")
    lang_collections = filter(lambda name: len(name) == 2, collections)
    print(f"Available codes: {' '.join(lang_collections)}")
    exit()

filename = sys.argv[1]
code_list = sys.argv[2:]

for code in code_list:
    # if code not in languages:
    #     print(f"Error: {code} is not a valid language code")
    #     exit()
    if code not in collections:
        print(f"Not found {code} corpus")
        exit()

sep = os.path.sep
corpora_dir = "corpora"
os.makedirs(corpora_dir, exist_ok=True)

_code_list = " ".join(code_list)
print(f"Export {_code_list} to: {corpora_dir}")

def sanitize(text):
    return re.sub(r'[\r\n\t\0]', ' ', text).replace("  ", " ", 1000).strip()

# Export parallel corpus to text files
def export(code):
    # Clear files before starting
    file_path = f"{corpora_dir}{sep}{filename}.{code}"
    open(file_path, "w", encoding='utf8').close()

    # Get min and max _id
    max_id = db[code].find_one({}, sort=[("_id", -1)])["_id"]
    total_docs = max_id - 1
    print(f"Processing {code} documents from {1:,} to {max_id:,} total {total_docs:,} documents")

    # Process in larger batches
    batch_size = 1000000  # Increased batch size for better performance
    total_batches = (total_docs + batch_size - 1) // batch_size
    batch_ranges = [(i * batch_size, min((i + 1) * batch_size, max_id + 1)) for i in range(total_batches)]

    # print(f"Starting export with {total_batches} batches...")

    for start_id, end_id in tqdm(batch_ranges, desc=f"Exporting {code} corpus"):

        cursor = db[code].find(
            {"_id": {"$gt": start_id, "$lte": end_id}},
            {code: 1},
            batch_size=batch_size
        ).sort("_id", 1)
        data = {doc["_id"]: sanitize(doc[code]) if code in doc and doc[code] else "" for doc in list(cursor)}

        lines = [data[_id] if _id in data else "" for _id in range(start_id + 1, end_id)]    
            
        # Write all lines at once
        with open(file_path, "a", encoding='utf8', buffering=8192) as f:
            f.write("\n".join(lines))

for code in code_list:
    export(code)

print(f"Successfully exported all corpora")
