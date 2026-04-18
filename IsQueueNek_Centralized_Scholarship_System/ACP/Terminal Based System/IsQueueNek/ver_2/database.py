import json
import os

def load_db(filepath):
    # If the database does not exist yet it returns an empty dictionary
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return {}
    with open(filepath, "r") as file:
        return json.load(file)
    
def save_db(data, filepath):
    with open(filepath, "w") as file:
        json.dump(data, file, indent =  4)