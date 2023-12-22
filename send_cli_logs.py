#!/usr/bin/python3
import json
import linecache
import os
# from elasticsearch import Elasticsearch
# from elasticsearch.exceptions import RequestError
from pathlib import Path
import random

import re
import sys
import base64
import calendar
import time
import pytz
from datetime import datetime
from dotenv import load_dotenv
import socket

import requests
def get_base_url(url, port):
    return "{}:{}".format(url, port)

# http request data
def load_env():
    load_dotenv(os.path.join(Path.home(), ".cyber-range-collector", ".env"))
    apiURL = os.getenv('APIURL')
    apiPORT = os.getenv('APIPORT')
    bearer = os.getenv('BEARER')
    return apiURL, apiPORT, bearer



def is_valid_timestamp(tmp):
    """
    Returns true if it is a valid timestamp in the form 10:29:11.734 (12 chars)
    """
    return len(tmp) == 12

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

    
OS_INDEX="crc-command"
def send_command_index(base_url, document):

    url = f"{base_url}/{OS_INDEX}"
    headers = {
    'Authorization': 'Bearer {}'.format(bearer),
    'Content-Type': 'application/json'
    }
    data = {
      'document' : document, 
    }
    response = requests.request("PUT", url, headers=headers, json=data)


def create_log(command, logs):
    content_without_escape_codes = remove_escape_codes(logs)
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
            tmp = removeNonAscii(timestamp)
            now = datetime.now()
            correct_date = now.date()
            if is_valid_timestamp(tmp):
                time_obj = datetime.combine(correct_date, datetime.strptime(tmp, '%H:%M:%S.%f').time())
                timezone = pytz.utc
                localized_time_obj = timezone.localize(time_obj)
                iso_time = localized_time_obj.isoformat()
            else:
                print("[-] not valid iso_time, will skip")
                iso_time = None
            
        except IndexError:
            timestamp = ""
        dirty_out = []
        i = 2
        while i < len(content_without_escape_codes[match.end():].split("\n")) and not content_without_escape_codes[match.end():].split("\n")[i].startswith("┌──"):
            dirty_out.append(remove_timestamps(removeNonAscii(content_without_escape_codes[match.end():].split("\n")[i].rstrip())))
            i += 1
        str_output="\n".join(dirty_out)
        output = re.sub(regex, '', str_output)
        if iso_time:
            return {
                "working_directory": working_directory,
                "timestamp": iso_time,
                "command": command,
                "output": output
            }



    


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("[-] Usage: send_cli_logs <session_id> <command> <logs_file>")
        sys.exit(-1)

    session_id = sys.argv[1]
    command = sys.argv[2]
    file = sys.argv[3]
    logs = ""
    apiURL, apiPORT, bearer = load_env()

    base_object = {
        'session_id' : session_id,
        'host_id' : socket.gethostname()
    }

    with open(file, 'r') as f:
        logs = f.read()
    the_log = create_log(command, logs)
    # Add log information
    base_object.update(the_log)
    base_url = get_base_url(apiURL, apiPORT)
    send_command_index(base_url, base_object)

    # pretty_json = json.dumps(the_log, indent=4)
    # with open('/tmp/basic_file.txt', 'w') as ff:
    #     ff.write(pretty_json)

    # print(pretty_json)
    
    # for line_number in range(first_line, last_line + 1):
    #     logs = logs +  linecache.getline(file, line_number)
    # the_log = create_log(command, logs)
    # print(the_log)
    
            
