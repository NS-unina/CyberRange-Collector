import re
import json
import shutil
import os
import base64
import calendar
import time

# This function checks if the filename is either .png or .jpg
def is_image_file(filename: str) -> bool:
    return filename.endswith(".png") or filename.endswith(".jpg")

# This function removes the NonAscii characters
def removeNonAscii(s): 
    return "".join(i for i in s if ord(i)<126 and ord(i)>31)

# This function can be used to remove extra timestamp inside the output
def remove_timestamps(input_string):
    timestamp_regex = r"\d{2}:\d{2}:\d{2}\.\d{3}"
    output_string = re.sub(timestamp_regex, "", input_string)
    return output_string

# This function converts the contents of the image file at file_path to a base64 encoded string
def convert_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

# This function removes escape codes from the input content string
def remove_escape_codes(content: str) -> str:
    return re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', content)

# This function moves all files in the folder that end with "_JSON" to a subfolder named "JSON"
def move_json_files(folder: str):
    # Check if the folder exists
    if not os.path.exists(folder):
        return

    # Create a new folder named "JSON" if it doesn't exist
    json_folder = os.path.join(folder, "JSON")
    if not os.path.exists(json_folder):
        os.mkdir(json_folder)

    # Search for files that end with "_JSON"
    for filename in os.listdir(folder):
        #if filename.endswith(s_time_stamp):
        if filename.endswith('.JSON'):
            file_path = os.path.join(folder, filename)
            shutil.move(file_path, json_folder)
            
# This function moves screenshot files into a subfolder called "screen"
def move_screen_files(folder: str):
    if not os.path.exists(folder):
        return

    screen_folder = './screen'

    # Search for the session files
    for filename in os.listdir(folder):
        if filename.endswith('.png'):
            file_path = os.path.join(folder, filename)
            shutil.move(file_path, screen_folder)

# This function processes all valid files in the folder and returns their file paths as a list
def process_folder(folder: str, is_valid_file: callable) -> list:
    files = []
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path) and is_valid_file(filename):
            files.append(file_path)
    return files

# This function processes a log file and returns a dictionary containing information extracted from the file
def process_log_file(command_path: str, log_path: str) -> dict:
    with open(command_path, "r") as cmd_f, open(log_path, "r") as log_f:
        logs = log_f.read()
        commands = cmd_f.readlines()
        index=0
        content_without_escape_codes = remove_escape_codes(logs)
        session_id = os.path.splitext(os.path.basename(log_path))[0]
        data = []
        regex = r'\]0;.*'
        matches = re.finditer(r"┌──[^\n]*\n", content_without_escape_codes)
        for match in matches:
            try:
                working_directory = match.group().split("[")[1].split("]")[0]
            except IndexError:
                working_directory = ""
            try:
                timestamp = content_without_escape_codes[match.end():].split("\n")[0]
                if (timestamp == ""):
                    continue
            except IndexError:
                timestamp = ""
            try:
                scorri = content_without_escape_codes[match.end():].split("\n")[1].split("$ ")[1]
                command = commands[index]
                index=index+1
            except IndexError:
                command = ""
            output_dirty = []
            i = 2
            while i < len(content_without_escape_codes[match.end():].split("\n")) and not content_without_escape_codes[match.end():].split("\n")[i].startswith("┌──"):
                output_dirty.append(remove_timestamps(removeNonAscii(content_without_escape_codes[match.end():].split("\n")[i].rstrip())))
                i += 1
            str_output="".join(output_dirty)
            output = re.sub(regex, '', str_output)
            data.append({
                "working_directory": working_directory,
                "timestamp": removeNonAscii(timestamp),
                "command": command[:-1],
                "output": output
            })
    return {session_id: data}

# Writes the given data to a JSON file in the specified folder
def write_to_json(data, folder, filename):
    json_file_path = os.path.join(folder, filename)
    with open(json_file_path, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)
        
# Rimuove le chiavi alle quali è associata una lista vuota da un dizionario        
def remove_empty_lists(d):
    for k, v in list(d.items()):  # utilizziamo list() per creare una copia delle chiavi del dizionario
        if isinstance(v, dict):
            remove_empty_lists(v)
        elif isinstance(v, list) and not v:
            del d[k]

def get_number_from_filename(path):
    filename = os.path.basename(path)
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    return 0
    
def sort_files_by_number(files):
    def get_file_number(file_path):
        # Estrarre il numero dal nome del file utilizzando una regex
        match = re.search(r'\d+', file_path)
        if match:
            return int(match.group())
        else:
            return float('inf')  # Se non ci sono numeri nel nome del file, mettilo alla fine dell'ordinamento
    
    return sorted(files, key=get_file_number)

def delete_files_with_extensions(directory, extensions):
    for filename in os.listdir(directory):
        if filename.endswith(extensions):
            os.remove(os.path.join(directory, filename))

screenshot_folder = './'

# Retrieves a list of screenshot files in the folder
screenshot_files = process_folder(screenshot_folder, is_image_file)
screenshots = [convert_to_base64(file_path) for file_path in screenshot_files]

log_folder = './logs'
files = os.listdir(log_folder)

# genero una lista di path di comandi e di log
txt_files = sorted([os.path.join(log_folder, f) for f in files if f.endswith(".txt")])
log_files = sorted([os.path.join(log_folder, f) for f in files if f.endswith(".log")])

# ordino la lista di path di comandi e di log
command_list = sort_files_by_number(txt_files)
log_list = sort_files_by_number(log_files)


# Stores the processed log data
data = {}
for commands, logs in zip(command_list, log_list):
    data.update(process_log_file(commands, logs))
    
remove_empty_lists(data)

# Combines the processed log data and the screenshots into a single dictionary
data_fin = {"host": data, "screenshots": screenshots}
current_GMT = time.gmtime()
time_stamp = calendar.timegm(current_GMT)
s_time_stamp = str(time_stamp)
json_filename = "JSON"+s_time_stamp+".JSON"
write_to_json(data_fin, log_folder, json_filename)

move_json_files(log_folder)
delete_files_with_extensions(log_folder, ('.txt', '.log'))
move_screen_files(screenshot_folder)
