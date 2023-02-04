import re
import json
import shutil
import os
import base64

def convert_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string


def remove_escape_codes(text):
    return re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)

def remove_formatting_chars(text):
    return re.sub(r'\u001b.*?m', '', text)
    
def move_json_files(directory):
    # Verifica che la directory esista
    if not os.path.exists(directory):
        return

    # Crea una nuova cartella chiamata "JSON" se non esiste
    json_folder = os.path.join(directory, "JSON")
    if not os.path.exists(json_folder):
        os.mkdir(json_folder)

    # Cerca i file che terminano per "_JSON"
    for filename in os.listdir(directory):
        if filename.endswith("_JSON"):
            file_path = os.path.join(directory, filename)
            shutil.move(file_path, json_folder)
            
screenshot_folder = '/home/kali/Documents/script'
screenshots = []
for filename in os.listdir(screenshot_folder):
	if filename.endswith(".png") or filename.endswith(".jpg"):
		file_path = os.path.join(screenshot_folder, filename)
		if os.path.isfile(file_path):
			base64_screenshot = convert_to_base64(file_path)
			screenshots.append(base64_screenshot)

folder = '/home/kali/Documents/script/log'
for filename in os.listdir(folder):
    if filename.endswith(".log"):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            with open(file_path) as f:
                content = f.read()
                prova = remove_escape_codes(content)
                data = []
                matches = re.finditer(r"┌──\(kali[^\n]*\)\-[^\n]*\n", prova) #guardare
                for match in matches:
                    timestamp = prova[match.end():].split("\n")[0]
                    command = prova[match.end():].split("\n")[1].split("$ ")[1]
                    output = []
                    i = 2
                    while i < len(prova[match.end():].split("\n")) and not prova[match.end():].split("\n")[i].startswith("┌──"):
                        output.append(prova[match.end():].split("\n")[i].rstrip())
                        i += 1
                    data.append({
                        "timestamp": timestamp,
                        "command": remove_formatting_chars(command),
                        "output": "\n".join(output)
                    })
                json_filename = os.path.splitext(filename)[0] + "_JSON"
                json_file_path = os.path.join(folder, json_filename)
                
                
                with open(json_file_path, 'w', encoding='utf8') as json_file:
                    data_fin = {"commands": data, "screenshots": screenshots}
                    json.dump(data_fin, json_file, ensure_ascii=False)
                    
move_json_files(folder)
