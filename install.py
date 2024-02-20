import os
import platform

def setup_library():
    cmd = "pip install -r requirements.txt"
    os.system(cmd)

def install_ngrok():
    import requests
    import tarfile
    import zipfile
    os_name = platform.system()
    architecture = platform.architecture()[0]
    if os_name == "Linux":
        print("Downloading ngrok for linux...")
        url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
        file_name = "ngrok.tgz"
    elif os_name == "Window" and architecture == "32bit":
        print("Downlading ngrok for window 32 bit...")
        url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-386.zip"
        file_name = "ngrok.zip"
    elif os_name == "Window" and architecture == "64bit":
        print("Downloading ngrok for window 64 bit...")
        url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
        file_name = "ngrok.zip"
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)
        if os_name == "Linux":
            with tarfile.open(file_name, "r:gz") as tar:
                tar.extractall()
            print("ngrok downloaded successfully.")
            os.remove(file_name)
        elif os_name == "Window":
            with zipfile.ZipFile(file_name, "r") as zip_ref:
                zip_ref.extractall()
            print("ngrok downloaded successfully.")
            os.remove(file_name)
    else:
        print("Failed to download the file.")

def setup_ngrok():
    print("Signup on this(https://dashboard.ngrok.com/signup) page and paste authtoken")
    token = input("Enter ngrok token ::: ")
    cmd = "./ngrok config add-authtoken {}".format(token)
    os.system(cmd)

install_ngrok()
setup_ngrok()







