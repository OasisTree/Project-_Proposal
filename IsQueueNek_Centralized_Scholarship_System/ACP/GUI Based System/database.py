import json
import os


def load_db(filepath):
    """Load JSON data from file; return empty dict if file is missing/empty."""

    # Avoid errors if file doesn't exist or is empty
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return {}

    with open(filepath, "r") as file:
        return json.load(file)


def save_db(data, filepath):
    """Save dictionary data to JSON file (overwrites existing content)."""

    # Write data to file with readable formatting
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)
