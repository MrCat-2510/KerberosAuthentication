from Key_Generate import create_privated_key
from cryptography.fernet import Fernet

Alice_name = 'Alice'
Alice_password = 123

Alice_key = create_privated_key(Alice_name, Alice_password)

Server_name = 'Server'
Server_password = 123

Server_key = create_privated_key(Server_name,Server_password)

def decrypted(key, ciphertext):
    try:
        if type(ciphertext) == str:
            ciphertext = ciphertext.encode()
        decrypted_text = Fernet(key).decrypt(ciphertext)
        return decrypted_text
    except:
        print('TICKET IS WRONG OR OUTDATED')