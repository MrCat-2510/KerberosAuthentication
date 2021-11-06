import time
from cryptography.fernet import Fernet
import base64
import os

def create_TGT_session_key(time, name):
    key = Fernet.generate_key()
    file = open(name, 'wb')
    file.write(key + ('/' + time).encode())
    file.close()
    return key

def create_Token_session_key(time):
    key = Fernet.generate_key()
    file = open('Token.key', 'wb')
    file.write(key + ('/' + time).encode())
    file.close()
    return key

def create_privated_key(name, password):
    MAX_LENGTH = 32
    text = name+str(password)
    key = base64.urlsafe_b64encode(text.encode()+ os.urandom(MAX_LENGTH - len(text)))
    return key

def convert_to_datetime(timestamp):
    # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)))
    # print(time.strftime('%S', time.localtime(timestamp)))
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))