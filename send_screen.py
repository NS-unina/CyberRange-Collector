#!/usr/bin/python3
import base64
import json
from pathlib import Path
import random
import socket
import sys
from dotenv import load_dotenv
import os
from datetime import datetime

import requests
import json

def get_base_url(url, port):
    return "{}:{}".format(url, port)



def index_exists(index_name, base_url):
    url = f"{base_url}/{index_name}"
    headers = {
    'Authorization': 'Bearer {}'.format(bearer),
    'Content-Type': 'application/json'
    }
    response = requests.head(url, headers = headers)
    return response.status_code == 200

# def create_index(index_name, base_url):
#     url = f"{base_url}/{index_name}"
#     headers = {
#     'Authorization': 'Bearer {}'.format(bearer),
#     'Content-Type': 'application/json'
#     }
#     print(url)
#     response = requests.put(url, headers=headers, data=json.dumps(DOCUMENT_MAPPING))
#     print(response.text)
#     print(response.status_code)
#     # return response.json()



def load_env():
    load_dotenv(os.path.join(Path.home(), ".cyber-range-collector", ".env"))
    apiURL = os.getenv('APIURL')
    apiPORT = os.getenv('APIPORT')
    bearer = os.getenv('BEARER')
    return apiURL, apiPORT, bearer

OS_INDEX="crc-screenshot"

def send_image(document):
    url = f"{apiURL}:{apiPORT}/openSearch/{OS_INDEX}"
    headers = {
    'Authorization': 'Bearer {}'.format(bearer),
    'Content-Type': 'application/json'
    }
    data = {
      'document' : document, 
    }
    # first = {"_index": OS_INDEX, "_id" : str(random.randint(10000, 99999))}
    # payload = []
    # payload.append({
    #     "create": first
    # })
    # payload.append(document)
    # send = json.dumps(payload)
    print("Data")
    response = requests.request("PUT", url, headers=headers, json=data)
    print(response.text)

    
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("[-] Usage: send_screen.py <win-name> <filename>")
        sys.exit(-1)

    win_name = sys.argv[1]
    filename = sys.argv[2]
    apiURL, apiPORT, bearer = load_env()

    encoded_string = encode_image_to_base64(filename)
    document = {
        'win_name' : win_name,
        'host_id' : socket.gethostname(),
        'timestamp': datetime.now().isoformat(),
        'image' : encoded_string
    }
    base_url = get_base_url(apiURL, apiPORT)
    # if not index_exists(OS_INDEX, base_url):
    #     create_index(OS_INDEX, base_url)
    # else:
    #     print("{} Already exists".format(OS_INDEX))

    print("[+] send document")
    send_image(document)
