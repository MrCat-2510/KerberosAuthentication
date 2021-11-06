import time

from Privated_Key import Server_key, decrypted
from Key_Generate import convert_to_datetime
from cryptography.fernet import Fernet
from KDC import LIFETIME_TOKEN
import sys

class Server:
    KDC_name = 'KerberosAuthentication'
    message = ""
    ACCEPT = False

    def __init__(self, message):
        self.message = message

    def authentication(self):
        A_Alice_Server, Token = self.message.split("||")
        Token_message = decrypted(Server_key, Token)
        if Token_message != False:
            KDC_name, Sender_name, self.timestamp, key_Alice_Server = decrypted(Server_key, Token).decode().split("||")
            if KDC_name == self.KDC_name:
                if ((time.time() - float(self.timestamp)) < LIFETIME_TOKEN):
                    decrypted_message = decrypted(key_Alice_Server, A_Alice_Server)
                    if decrypted_message != False:
                        name, timesending = decrypted_message.decode().split("||")
                        if name == Sender_name:
                            print(convert_to_datetime(time.time()), " Authentication in Server Complete || Server")
                            Server_response_text = str(float(timesending) + 1)
                            Server_response = Fernet(key_Alice_Server).encrypt(Server_response_text.encode()).decode()
                            return Server_response
                        else:
                            print(convert_to_datetime(time.time())," Name is not correct!!! || Server")
                            return "0||0"
                    else:
                        print(convert_to_datetime(time.time()), " Cannot decrypted message by Secret key || Server")
                        return "0||0"
                else:
                    print(convert_to_datetime(time.time()), " TOKEN IS OUTDATED || Server")
                    return "0||0"
            else:
                print(convert_to_datetime(time.time()), " Wrong KDC system name!!! || Server")
                return "0||0"
        else:
            print(convert_to_datetime(time.time()), " Cannot decrypted message with Server_key || Server")
            return "0||0"



