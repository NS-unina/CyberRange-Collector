import re
import json
import shutil
import os
import base64

# This function checks if the filename is either .png or .jpg
def is_image_file(filename: str) -> bool:
    return filename.endswith(".png") or filename.endswith(".jpg")

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
        if filename.endswith("_JSON"):
            file_path = os.path.join(folder, filename)
            shutil.move(file_path, json_folder)

# This function processes all valid files in the folder and returns their file paths as a list
def process_folder(folder: str, is_valid_file: callable) -> list:
    files = []
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path) and is_valid_file(filename):
            files.append(file_path)
    return files

# This function processes a log file and returns a dictionary containing information extracted from the file
def process_log_file(file_path: str) -> dict:
    with open(file_path) as f:
        content = f.read()
        content_without_escape_codes = remove_escape_codes(content)
        session_id = os.path.splitext(os.path.basename(file_path))[0]
        data = []
        matches = re.finditer(r"┌──\(kali[^\n]*\)\-[^\n]*\n", content_without_escape_codes)
        for match in matches:
            working_directory = match.group().split("[")[1].split("]")[0]
            timestamp = content_without_escape_codes[match.end():].split("\n")[0]
            command = content_without_escape_codes[match.end():].split("\n")[1].split("$ ")[1]
            output = []
            i = 2
            while i < len(content_without_escape_codes[match.end():].split("\n")) and not content_without_escape_codes[match.end():].split("\n")[i].startswith("┌──"):
                output.append(content_without_escape_codes[match.end():].split("\n")[i].rstrip())
                i += 1
            data.append({
                "working_directory": working_directory,
                "timestamp": timestamp,
                "command": command,
                "output": "\n".join(output)
            })
    return {session_id: data}

# Writes the given data to a JSON file in the specified folder
def write_to_json(data, folder, filename):
    json_file_path = os.path.join(folder, filename)
    with open(json_file_path, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)

screenshot_folder = './'
# Retrieves a list of screenshot files in the folder
screenshot_files = process_folder(screenshot_folder, is_image_file)
screenshots = [convert_to_base64(file_path) for file_path in screenshot_files]

log_folder = './log'
log_files = process_folder(log_folder, lambda x: x.endswith(".log"))

# Stores the processed log data
data = {}
for file_path in log_files:
    data.update(process_log_file(file_path))

# Combines the processed log data and the screenshots into a single dictionary
data_fin = {"host": data, "screenshots": screenshots}
json_filename = "host_JSON"
write_to_json(data_fin, log_folder, json_filename)

move_json_files(log_folder)