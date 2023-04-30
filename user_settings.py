import json

# Create a dictionary to store the data
data = {
    "production_steps": [{"name":"Fill","color":'red'},{"name":"Boil","color":"green"},{"name":"Clean","color":"blue"}],

}

# Convert the dictionary to a JSON string
json_data = json.dumps(data)

# Save the JSON string to a file
with open("data.json", "w") as f:
    f.write(json_data)