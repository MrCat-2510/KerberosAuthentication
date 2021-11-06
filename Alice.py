import time
from KDC import Authentication_Server, Ticket_Granting_Server
from Privated_Key import Alice_key, decrypted
from Key_Generate import convert_to_datetime
from cryptography.fernet import Fernet
from Server import Server
import sys

class Alice():

    SessionKey_Alice_TGS = b""
    TGS_message = ""
    timesending_to_TGS = 0.0
    def get_Token(self):
        stdoutOrigin = sys.stdout
        sys.stdout = open("log.txt", "w")
        # -----------------Alice&AS--------------------------#
        print("-----------------Alice&AS--------------------------")
        print(convert_to_datetime(time.time()), ': This is Alice Privated key: \n', Alice_key, "\n")
        print(convert_to_datetime(time.time()), " ====> SENDING\n")
        message = 'Alice||AuthenticationServer'
        encrypted_message_AS = Fernet(Alice_key).encrypt(message.encode())
        print(convert_to_datetime(time.time()), " Encrypted request to Authentication server: \n", encrypted_message_AS, "\n")

        AS = Authentication_Server(encrypted_message_AS)

        print(convert_to_datetime(time.time())," RECEIVED <===\n")

        encrypted_response_AS = AS.AS_authentication()
        print(convert_to_datetime(time.time()), " Encrypted response from Authentication server: \n",encrypted_response_AS, "\n")

        response_array = encrypted_response_AS.split("||")

        self.SessionKey_Alice_TGS = decrypted(Alice_key, response_array[0])
        TGT = response_array[1]

        print(convert_to_datetime(time.time()), " Session key between Alice and TGS: \n", self.SessionKey_Alice_TGS, "\n")
        print(convert_to_datetime(time.time()), " Ticket Granting Ticket: \n", TGT, "\n")
        print("\n")
        # -----------------Alice&TGS--------------------------#
        print("-----------------Alice&TGS--------------------------")
        print(convert_to_datetime(time.time()), " ====> SENDING\n")
        self.timesending_to_TGS = time.time()
        A_Alice_TGS = Fernet(self.SessionKey_Alice_TGS).encrypt(("Alice||" + str(self.timesending_to_TGS)).encode()).decode()

        encrypted_message_TGS = "TicketGrantingserver||" + A_Alice_TGS + "||" + TGT

        print(convert_to_datetime(time.time()), " Encrypted request to Ticket Granting Server: \n", encrypted_message_TGS,"\n")

        TGS = Ticket_Granting_Server(encrypted_message_TGS)

        print(convert_to_datetime(time.time()), " RECEIVED<===\n")
        encrypted_response_TGS = TGS.TGS_authentication()

        print(convert_to_datetime(time.time()), " Encrypted response from Ticket Granting Server: \n",encrypted_response_TGS, "\n")

        TGS_name, self.TGS_message, Token = encrypted_response_TGS.split("||")

        print(convert_to_datetime(time.time()), " Token Ticket: \n",Token, "\n")
        print("\n")
        return Token

        sys.stdout.close()
        sys.stdout = stdoutOrigin
    def get_access(self, Token):
        stdoutOrigin = sys.stdout
        sys.stdout = open("log.txt", "a")
        # -----------------Alice&Server--------------------------#
        print("-----------------Alice&Server--------------------------")

        SessionKey_Alice_Server = decrypted(self.SessionKey_Alice_TGS, self.TGS_message)
        timesending_to_Server = time.time()

        A_Alice_Server = Fernet(SessionKey_Alice_Server).encrypt(("Alice||" + str(self.timesending_to_TGS)).encode()).decode()
        server_message = A_Alice_Server + "||" + Token

        print(convert_to_datetime(time.time()), " Encrypted request to access to Server: \n", server_message, "\n")

        print(convert_to_datetime(time.time()), " ====> SENDING\n")

        server = Server(server_message)
        Server_response = server.authentication()

        print(convert_to_datetime(time.time())," RECEIVED <===\n")
        print(convert_to_datetime(time.time()), " Encrypted response  from Server: \n", Server_response, "\n")
        if Server_response == "0||0":
            return False
        else:
            Server_response_decrypted = Fernet(SessionKey_Alice_Server).decrypt(Server_response.encode())
            timedistance = float(Server_response_decrypted) - timesending_to_Server
            if timedistance <= 1:
                print(convert_to_datetime(time.time()), " The time of authentication: ", timedistance)
                print(convert_to_datetime(time.time()), ' KERBEROS AUTHENTICATION COMPLETE')
                return True
            else:
                print(convert_to_datetime(time.time()), ' KERBEROS AUTHENTICATION FAILED')
                return False



        sys.stdout.close()
        sys.stdout = stdoutOrigin








