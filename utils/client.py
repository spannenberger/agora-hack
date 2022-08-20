import json

with open('models/source/product_matches_path.json', 'r') as f:
    data = json.load(f)

def model2client(model_id):
    return data[model_id]