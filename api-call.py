import requests, json, random, shutil, os, re
import imageio.v2 as imageio


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

# function to extract the timestamp value from the file name
def get_timestamp(value):
    match = re.search(regex, value)
    if match:
        date_string = match.group()
        return(date_string)

# timestamp to find into the name string of the file
regex = r"\d{4}-\d{2}-\d{2}-\d{2}:\d{2}:\d{2}"

# information lists
session = []
directory = []
timestamp = []
command = []
output = []

# fill the lists with information from the dictionary
for session_name, session_items in session_data.items():
    for item in session_items:
        session.append(session_name)
        directory.append(item['working_directory'])
        timestamp.append(item['timestamp'])
        command.append(item['command'])
        output.append(item['output'])

# http request data
url_bulk = "http://localhost:9000/openSearch/bulk"
headers = {
  'Authorization': 'Bearer 30e16f01ffc18fbc019eaac098628cdcd3b596f43bcd5937958842f77a8d4fa5',
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

response = requests.request("POST", url_bulk, headers=headers, data=send)

print(response.text)

move_json_files(log_folder)

url_gif = f"http://localhost:9000/images/upload/{host}"
folder_path = "./screen" # specificare il percorso della cartella contenente i file

images = [img for img in os.listdir(folder_path) if img.endswith('.png')]
gif_file = f'./screen/{host}.gif'

with imageio.get_writer(gif_file, mode='I', duration=0.5) as writer:
    for image_name in sorted(images, key = get_timestamp):
        image_path = os.path.join(folder_path, image_name)
        image = imageio.imread(image_path)
        writer.append_data(image)
    

files = {}
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        files[filename] = open(file_path, "rb")

headers = {
  'Authorization': 'Bearer 30e16f01ffc18fbc019eaac098628cdcd3b596f43bcd5937958842f77a8d4fa5',
}

response = requests.post(url_gif, headers=headers, files=files)

json = response.json()
print(json)

# chiudiamo tutti i file aperti
for file in files.values():
    file.close()
