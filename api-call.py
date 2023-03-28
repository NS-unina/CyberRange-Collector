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
url = "https://localhost:9200/_bulk"
headers = {
  'Authorization': 'Basic YWRtaW46YWRtaW4=',
  'Content-Type': 'application/json'
}

payload = ""
for index in range(len(session)):
    first = "{ \"create\": { \"_index\": \"command\", \"_id\": \"" + str(random.randint(10000, 99999)) + "\" } }\n"
    payload += first 
    host_str = "{ \"host_id\": \"" + str(random.randint(1,1000)) + "\","
    session_str =  "\"session_id\": \"" + str(session[index]) + "\"," 
    directory_str = "\"working_directory\": \"" + str(directory[index]) + "\","
    timestamp_str = "\"timestamp\": \"" + str(timestamp[index]) + "\"," 
    command_str = "\"command\": \"" + str(command[index]) + "\","
    output_str = "\"output\": \"" + str(output[index]) + "\" }\n"
    second = host_str + session_str + directory_str + timestamp_str + command_str + output_str
    payload += second

print(payload)

#response = requests.request("POST", url, headers=headers, data=payload, verify=False)

#print(response.text)

move_json_files(log_folder)
