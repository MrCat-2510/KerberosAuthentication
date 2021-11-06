import time
from Key_Generate import create_TGT_session_key,create_Token_session_key ,convert_to_datetime, create_privated_key
from Privated_Key import Alice_key, Server_key, decrypted
from cryptography.fernet import Fernet
import sys

KDC_name = 'KerberosAuthentication'
password = 123
KDC_key = create_privated_key(KDC_name,password)
LIFETIME_TGT = 120
LIFETIME_TOKEN = 60


class Authentication_Server:
    server_name = "AuthenticationServer"
    message = ""
    CONFIRM = False
    Sender_name = ""

    def __init__(self, message):
        self.message = Fernet(Alice_key).decrypt(message).decode()

    def AS_authentication(self):
        self.Sender_name, system_name = self.message.split("||")
        if(system_name == self.server_name):
            print(convert_to_datetime(time.time()), ' Authentication Success. Create session key and TGT || AS')
            self.CONFIRM = True
            current_time = time.time()
            key_Alice_TGS, current_time = Session_key(self.CONFIRM, "TGT.key", current_time)
            TGT_string = KDC_name + "||" + self.Sender_name + "||" + str(current_time) + "||" + key_Alice_TGS
            TGT = Fernet(KDC_key).encrypt(TGT_string.encode()).decode()
            AS_response = Fernet(Alice_key).encrypt(key_Alice_TGS.encode()).decode() + "||" + TGT
            return AS_response
        else:
            print(convert_to_datetime(time.time()), ' Authentication Failed. Wrong server name || AS')
            self.CONFIRM = False
            return "None||None"



class Ticket_Granting_Server:
    name_server = "TicketGrantingserver"
    message = ""
    CONFIRM = False
    current_time = 0.0
    def __init__(self, message):
        self.message = message
    def TGS_authentication(self):
        name,A_Alice_TGS,TGT = self.message.split("||")
        if name == self.name_server:
            self.CONFIRM = True
            Server,Sender_name,timestamp,key_A_TGS = decrypted(KDC_key, TGT).decode().split("||")
            if Server == KDC_name:
                if ((time.time() - float(timestamp)) < LIFETIME_TGT):
                    decrypted_message = decrypted(key_A_TGS, A_Alice_TGS)
                    if decrypted_message != False:
                        name, timesending = decrypted_message.decode().split("||")
                        if Sender_name == name:
                            print(convert_to_datetime(time.time()), ' AUTHENTICATION IN TGT COMPLETE || TGS')
                            current_time = time.time()
                            key_Alice_Server, current_time = Session_key(self.CONFIRM,'Token.key', current_time)
                            Token_string = KDC_name + "||" +Sender_name +"||" + str(current_time) + "||" + key_Alice_Server
                            Token = Fernet(Server_key).encrypt(Token_string.encode()).decode()
                            TGS_response = Sender_name + "||" + Fernet(key_A_TGS).encrypt(key_Alice_Server.encode()).decode() + "||" + Token
                            return TGS_response
                        else:
                            print(convert_to_datetime(time.time()), " WRONG SENDER NAME!!! || TGS")
                            return "0||0||0"
                    else:
                        print(convert_to_datetime(time.time()), " The session key between User and TGS cannot decrypt this message!!! || TGS")
                        return "0||0||0"
                else:
                    print(convert_to_datetime(time.time()), " TGT IS OUTDATED!!! || TGS")
                    return "0||0||0"
            else:
                print(convert_to_datetime(time.time()), " WRONG SYSTEM NAME!!! || TGS")
                return "0||0||0"

        else:
            print(convert_to_datetime(time.time()), ' Authentication Failed. Wrong server name!!! || TGS')
            self.CONFIRM = False
            return "0||0||0"

def Session_key(CONFIRM, name, current_time):
    if(CONFIRM == True):
        try:
            file = open(name, 'rb').read()
        except:
            first_key = create_TGT_session_key(str(current_time), name)
            return first_key.decode()
        old_key, old_time = file.decode().split('/')
        # convert_to_datetime(float(old_time))
        # convert_to_datetime(current_time)
        if((current_time - float(old_time))> LIFETIME_TOKEN):
            print(convert_to_datetime(time.time()), ' +++++++{} is OUTDATED+++++++\n'.format(name))
            newkey = create_TGT_session_key(str(current_time),name)
            return newkey.decode(), current_time
        else:
            print(convert_to_datetime(time.time()), ' -------{} is NOT outdated-------\n'.format(name))
            return old_key, old_time
    else:
        print(convert_to_datetime(time.time()), " This user has wrong information")
        return "None||None"


def check_Token_status(Token):
    stdoutOrigin = sys.stdout
    sys.stdout = open("log.txt", "a")
    Token_message = decrypted(Server_key, Token)
    if Token_message != False:
        KDC_name, Sender_name, timestamp, key_Alice_Server = decrypted(Server_key, Token).decode().split("||")
        if KDC_name == KDC_name:
            currenttime = time.time()
            if ((currenttime - float(timestamp)) < LIFETIME_TOKEN):
                print(convert_to_datetime(time.time()), " TOKEN IS NOT OUTDATED YET || STATUS")
                lefttime = currenttime - float(timestamp)
                lefttime = LIFETIME_TOKEN - int(lefttime % 60)
                timestamp = convert_to_datetime(float(timestamp))
                return timestamp, lefttime
            else:
                print(convert_to_datetime(time.time()), " TOKEN IS OUTDATED || STATUS")
                return None, None
        else:
            print(convert_to_datetime(time.time()), " Wrong KDC system name!!! || STATUS")
            return None, None
    else:
        print(convert_to_datetime(time.time()), " Cannot decrypted message with Server_key || STATUS")
        return None, None
    sys.stdout.close()
    sys.stdout = stdoutOrigin