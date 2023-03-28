import requests
import json
import random

# Prelevo i dati dal file JSON (generalizzare su tutti i file JSON o su un file JSON generico) e creo un dizionario con tali dati
with open('test.json') as f:
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

payload = []
for index in range(len(session)):
    first = "{ \"create\": { \"_index\": \"command\", \"_id\": \"" + str(random.randint(10000, 99999)) + "\" } }\n"
    payload.append(first) 
    host_str = "{ \"host_id\": \"" + str(random.randint(1,1000)) + "\","
    session_str =  "\"session_id\": \"" + str(session[index]) + "\"," 
    directory_str = "\"working_directory\": \"" + str(directory[index]) + "\","
    timestamp_str = "\"timestamp\": \"" + str(timestamp[index]) + "\"," 
    command_str = "\"command\": \"" + str(command[index]) + "\","
    output_str = "\"output\": \"" + str(output[index]) + "\" }\n"
    second = host_str + session_str + directory_str + timestamp_str + command_str + output_str
    payload.append(second)

payload_json = json.dumps(payload)

print(payload_json)

#response = requests.request("POST", url, headers=headers, data=payload_json, verify=False)
#print(response.text)