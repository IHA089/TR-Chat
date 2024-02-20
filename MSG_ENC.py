from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import random

kd = ['a', 'm', 'y', 'K', 'W']
k9 = ['b', 'n', 'z', 'L', 'X']
kc = ['c', 'o', 'A', 'M', 'Y']
k6 = ['d', 'p', 'B', 'N', 'Z']
k3 = ['e', 'q', 'C', 'O', '!']
k0 = ['f', 'r', 'D', 'P', '@']
k4 = ['g', 's', 'E', 'Q', '#']
k7 = ['h', 't', 'F', 'R', '$']
k8 = ['i', 'u', 'G', 'S']
k2 = ['j', 'v', 'H', 'T']
k1 = ['k', 'w', 'I', 'U']
k5 = ['l', 'x', 'J', 'V']

def GEN_AES_256_KEY():
    return os.urandom(32)

def RSA_KEY_GEN():
    key = RSA.generate(2048)
    public_key = key.publickey()
    private_key = key
    return public_key, private_key

def RSA_ENC(key, msg):
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(msg)
    return ciphertext

def RSA_DEC(key, msg):
    cipher = PKCS1_OAEP.new(key)
    decrypted_message = cipher.decrypt(msg)
    return decrypted_message

def KEY_ENC(data):
    ndata=""
    for char in data:
        if char == "0":
            ndata = ndata+random.choice(k0)
        elif char == "1":
            ndata = ndata+random.choice(k1)        
        elif char == "2":
            ndata = ndata+random.choice(k2)
        elif char == "3":
            ndata = ndata+random.choice(k3)
        elif char == "4":
            ndata = ndata+random.choice(k4)
        elif char == "5":
            ndata = ndata+random.choice(k5)
        elif char == "6":
            ndata = ndata+random.choice(k6)
        elif char == "7":
            ndata = ndata+random.choice(k7)
        elif char == "8":
            ndata = ndata+random.choice(k8)
        elif char == "9":
            ndata = ndata+random.choice(k9)
        elif char == ".":
            ndata = ndata+random.choice(kd)
        elif char == ":":
            ndata = ndata+random.choice(kc)
    return ndata

def KEY_DEC(data):
    ndata = ""
    for char in data:
        if char in k0:
            ndata = ndata+"0"
        elif char in k1:
            ndata = ndata+"1"
        elif char in k2:
            ndata = ndata+"2"
        elif char in k3:
            ndata = ndata+"3"
        elif char in k4:
            ndata = ndata+"4"
        elif char in k5:
            ndata = ndata+"5"
        elif char in k6:
            ndata = ndata+"6"
        elif char in k7:
            ndata = ndata+"7"
        elif char in k8:
            ndata = ndata+"8"
        elif char in k9:
            ndata = ndata+"9"
        elif char in kd:
            ndata = ndata+"."
        elif char in kc:
            ndata = ndata+":"
    return ndata

def AES_256_ENCRYPT(key, plaintext):
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return iv + ciphertext

def AES_256_DECRYPT(key, ciphertext):
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext