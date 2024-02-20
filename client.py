import socket
import sys
import threading
import os
import MSG_UI
import MSG_ENC
import platform

sender_data = "\rType : "

try:
    import msvcrt  
except ImportError:
    import tty     
    import termios

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
else:
    def getch():
        return msvcrt.getch().decode()

def updater():
    global sender_data
    print("\r"+"Type : "+sender_data, end="")

def Reciver(client, key):
    while True:
        try:
            byte_data = client.recv(1024)
            dec_data = MSG_ENC.AES_256_DECRYPT(key, byte_data)
            str_dec_data = str(dec_data, 'utf-8')
            str_dec_data = str_dec_data.split("<IHA089>")
            name = str_dec_data[0]
            message = str_dec_data[1]
            ll = len(sender_data)
            print("\r" + " "*(ll+7), end="")
            UI_MSG = MSG_UI.L_BOX(message, name)
            print(UI_MSG)
            updater()
        except OSError:
            return

def writer(client, key):
    os_name = platform.system()
    global sender_data
    input_data = ""
    while True:
        try:
            char = getch()
            if char == '\r':
                input_data = ""
                if sender_data == "":
                    pass
                else:
                    if sender_data == "exit" or sender_data == "Exit" or sender_data == "EXIT":
                        print("\rExiting...")
                        client.close()
                        break
                    else:
                        byte_sender_data=bytes(sender_data, 'utf-8')
                        enc_sender_data = MSG_ENC.AES_256_ENCRYPT(key, byte_sender_data)
                        client.send(enc_sender_data)
                        UI_MSG = MSG_UI.R_BOX(sender_data, "you")
                        print(UI_MSG)
                        sender_data = input_data
            elif os_name == "Linux" and char == '\x7f': 
                input_data = input_data[:-1]
                sender_data = input_data+"\x7f"+" "
                print("\r"+sender_data, end="")
            elif os_name == "Window" and char == "\b":
                input_data = input_data[:-1]
                sender_data = input_data+"\b"+" "
                print("\r"+sender_data, end="")
            else:
                input_data = input_data+char
                sender_data = input_data
            updater()    
        except KeyboardInterrupt:
            sys.exit()
    sys.exit()

name = input("Enter your name : ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
key = input("Enter Key ::: ")
get_key = MSG_ENC.KEY_DEC(key)
get_con = get_key.split(":")

try:
    client.connect((get_con[0], int(get_con[1])))
except ConnectionRefusedError:
    print("Invalid key, connection refused")
    sys.exit()
client.send(bytes(name, 'utf-8'))
data = client.recv(1024)
data = str(data, 'utf-8')
if data == "accept":
    print("connected with server")
    pub_key, pri_key = MSG_ENC.RSA_KEY_GEN()
    dd = pub_key.export_key()
    client.send(dd)
    enc_enc_key = client.recv(1024)
    ENC_KEY = MSG_ENC.RSA_DEC(pri_key, enc_enc_key)
    rec = threading.Thread(target = Reciver, args=(client, ENC_KEY))
    rec.start()
    writer(client, ENC_KEY)
    rec.join()
    sys.exit()
elif data == "decline":
    print("Server decline your request")
    client.close()
    sys.exit()
elif data == "avail":
    print("{} is already given, please provide different name".format(name))
    client.close()
    sys.exit()
else:
    print("Failed to connect")
    client.close()
    sys.exit()