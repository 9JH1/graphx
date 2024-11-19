import json
import uuid  # For generating unique IDs

# Example data to append
data = {"key1": "value1", "key2": "value2"}
file_path = "./index.json"

# Load the existing JSON file
with open(file_path, "r") as file:
    existing_data = json.load(file)

# Ensure the "images" key exists
if "images" not in existing_data:
    existing_data["images"] = {}

# Generate a unique ID and append the new data
new_id = str(uuid.uuid4())  # Generate a new unique ID
existing_data["images"][new_id] = data

# Write the updated data back to the file
with open(file_path, "w") as file:
    json.dump(existing_data, file, indent=2)
