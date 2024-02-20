import subprocess
import threading
import requests
import socket
import json
import sys
from time import sleep

def create_public_connection():
    command = "./ngrok tcp 8089"
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def CRT_PUB_CON():
    publicthread = threading.Thread(target = create_public_connection)
    publicthread.start()
    sleep(1)
    get_data_url = "http://localhost:4040/api/tunnels"
    get_data_req = requests.get(get_data_url)
    if get_data_req.status_code == 200:
        data = get_data_req.text
        json_data = json.loads(data)
        public_url = json_data['tunnels'][0]['public_url']
        public_url = public_url.replace("tcp://","")
        public_ul = public_url.split(":")
        hostname = public_ul[0]
        IP = socket.gethostbyname(hostname)
        public_url = public_url.replace(hostname, IP)
        return public_url
    else:
        print("Failed to create public connection...")
        print("Try again")
        sys.exit()        