import requests
import json
import random
import shutil
import os

# This function moves all files in the folder that end with ".JSON" to a subfolder named "JSON"
def move_json_files(folder: str):
    if not os.path.exists(folder):
        return

    # Create a new folder named "JSON" if it doesn't exist
    json_folder = os.path.join(folder, "JSON")
    if not os.path.exists(json_folder):
        os.mkdir(json_folder)

    # Search for files that end with ".JSON"
    for filename in os.listdir(folder):
        if filename.endswith('.JSON'):
            file_path = os.path.join(folder, filename)
            shutil.move(file_path, json_folder)

# Prelevo i dati dal file JSON (generalizzare su tutti i file JSON o su un file JSON generico) e creo un dizionario con tali dati
log_folder = './logs'
for filename in os.listdir(log_folder):
    if filename.endswith('.JSON'):
        json_path = os.path.join(log_folder, filename)
        with open(json_path) as f:
            data = json.load(f)

session_data = {}
for session_name, session_items in data['host'].items():
    for item in session_items:
        item['session_name'] = session_name
        session_data.setdefault(session_name, []).append(item)

# Scorro il dizionario per generarmi le liste di informazioni
session = []
directory = []
timestamp = []
command = []
output = []


for session_name, session_items in session_data.items():
    for item in session_items:
        session.append(session_name)
        directory.append(item['working_directory'])
        timestamp.append(item['timestamp'])
        command.append(item['command'])
        output.append(item['output'])

# Dati della richiesta HTTPS
url = "http://localhost:9000/openSearch/bulk"
headers = {
  'Authorization': 'Bearer ',
  'Content-Type': 'application/json'
}

payload = []
host = str(random.randint(1,1000))
for index in range(len(session)):
    first = {"_index": "command" , "_id" : str(random.randint(10000, 99999))}
    payload.append({
        "create" : first
    })
    second = {
        "host_id": host, 
        "session_id" : str(session[index]), 
        "working_directory": str(directory[index]), 
        "timestamp": str(timestamp[index]),
        "command": str(command[index]),
        "output": str(output[index])
        }
    payload.append(second)

#print(payload)
send = json.dumps(payload)

response = requests.request("POST", url, headers=headers, data=send)

print(response.text)

move_json_files(log_folder)