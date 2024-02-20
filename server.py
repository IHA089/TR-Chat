import os
import socket
import threading
import PUB_CON
import MSG_ENC
from Crypto.PublicKey import RSA

def handle_client(client_socket, client_address, name, key):
    print(f"{name} connected successfully")
    for c in clients:
        if c != client_socket:
            new_data = bytes("server<IHA089>" +name+" connected successfully", 'utf-8')
            new_enc_data = MSG_ENC.AES_256_ENCRYPT(key, new_data)
            c.sendall(new_enc_data)
    while True:
        try:
            data = client_socket.recv(1024)
            data = MSG_ENC.AES_256_DECRYPT(key, data)
            data = str(data, 'utf-8')
            if not data:
                break
            for c in clients:
                if c != client_socket:
                    new_data = bytes(name+"<IHA089>"+data, 'utf-8')
                    new_enc_data = MSG_ENC.AES_256_ENCRYPT(key, new_data)
                    c.sendall(new_enc_data)
        
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break
    
    client_socket.close()
    clients.remove(client_socket)
    for c in clients:
        leave_msg = "server<IHA089>" + name + " leave this chat"
        new_leave_msg = MSG_ENC.AES_256_ENCRYPT(key, bytes(leave_msg,'utf-8'))
        c.sendall(new_leave_msg)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8089))

server_socket.listen(5)
get_key = PUB_CON.CRT_PUB_CON()
key = MSG_ENC.KEY_ENC(get_key)
ENC_KEY = MSG_ENC.GEN_AES_256_KEY()
print("Shared Key ::: {}".format(key))
print("Server is listening for incoming connections...")

clients = []
names = []

try:
    while True:
        client_socket, client_address = server_socket.accept()
        name = str(client_socket.recv(1024), 'utf-8')
        if name in names:
            client_socket.send(bytes("avail", 'utf-8'))
            client_socket.close()
        else:
            acceptable = input("Do you want to accept {} [y/n/] : ".format(name))
            if acceptable == 'y' or acceptable == "Y":
                client_socket.send(bytes("accept", 'utf-8'))
                get_pub_key_str = str(client_socket.recv(1024), 'utf-8')
                public_key = RSA.import_key(get_pub_key_str)
                enc_enc_key = MSG_ENC.RSA_ENC(public_key, ENC_KEY)
                client_socket.send(enc_enc_key)
                clients.append(client_socket)
                names.append(name)
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, name, ENC_KEY))
                client_thread.start()
            else:
                client_socket.send(bytes("decline", 'utf-8'))
                client_socket.close()

except KeyboardInterrupt:
    print("Server shutting down...")
    for client_socket in clients:
        client_socket.close()
    server_socket.close()
