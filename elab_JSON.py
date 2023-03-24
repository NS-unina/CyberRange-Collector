import re
import json
import shutil
import os
import base64
import calendar
import time
import pytz
from datetime import datetime

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
            
# This function moves screenshot files into a subfolder called "screen"
def move_screen_files(folder: str):
    if not os.path.exists(folder):
        return

    screen_folder = './screen'

    # Search for the screenshot files
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
                tmp = removeNonAscii(timestamp)
                now = datetime.now()
                correct_date = now.date()
                time_obj = datetime.combine(correct_date, datetime.strptime(tmp, '%H:%M:%S.%f').time())
                timezone = pytz.utc
                localized_time_obj = timezone.localize(time_obj)
                iso_time = localized_time_obj.isoformat()
                if (timestamp == ""):
                    continue
            except IndexError:
                timestamp = ""
            try:
                command = commands[index]
                index=index+1
            except IndexError:
                command = ""
            dirty_out = []
            i = 2
            while i < len(content_without_escape_codes[match.end():].split("\n")) and not content_without_escape_codes[match.end():].split("\n")[i].startswith("┌──"):
                dirty_out.append(remove_timestamps(removeNonAscii(content_without_escape_codes[match.end():].split("\n")[i].rstrip())))
                i += 1
            str_output="".join(dirty_out)
            output = re.sub(regex, '', str_output)
            data.append({
                "working_directory": working_directory,
                "timestamp": iso_time,
                "command": command[:-1],
                "output": output
            })
    return {session_id: data}

# Writes the given data to a JSON file in the specified folder
def write_to_json(data, folder, filename):
    json_file_path = os.path.join(folder, filename)
    with open(json_file_path, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

# This function sorts files by the number in the filename
def sort_files_by_number(files):
    def get_file_number(file_path):
        # Extract the number from the filename using a regex
        match = re.search(r'\d+', file_path)
        if match:
            return int(match.group())
        else:
            return float('inf')  # If there are no numbers in the filename, put it at the end of the sort
    
    return sorted(files, key=get_file_number)

# This function deletes files with a specific extension
def delete_files_with_extensions(directory, extensions):
    for filename in os.listdir(directory):
        if filename.endswith(extensions):
            os.remove(os.path.join(directory, filename))

screenshot_folder = './'

# Retrieves a list of screenshot files in the folder and convert them to base64
screenshot_files = process_folder(screenshot_folder, is_image_file)
screenshots = [convert_to_base64(file_path) for file_path in screenshot_files]

log_folder = './logs'
files = os.listdir(log_folder)

# Generate a list of path for commands and logs
txt_files = sorted([os.path.join(log_folder, f) for f in files if f.endswith(".txt")])
log_files = sorted([os.path.join(log_folder, f) for f in files if f.endswith(".log")])

# Sort the two lists of commands and logs
command_list = sort_files_by_number(txt_files)
log_list = sort_files_by_number(log_files)

# Stores the processed log data
data = {}
for commands, logs in zip(command_list, log_list):
    data.update(process_log_file(commands, logs))

# Combines the processed log data and the screenshots into a single dictionary
data_fin = {"host": data}#, "screenshots": screenshots}
current_GMT = time.gmtime()
time_stamp = calendar.timegm(current_GMT)
s_time_stamp = str(time_stamp)
json_filename = "JSON"+s_time_stamp+".JSON"
write_to_json(data_fin, log_folder, json_filename)

# Delete logs and commands file
delete_files_with_extensions(log_folder, ('.txt', '.log'))

# Move screenshot files into a specific folder
move_screen_files(screenshot_folder)
