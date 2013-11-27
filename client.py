'''
    3780 Networking Project
    Rio Lowry
'''
 
import socket   #for sockets
import sys  #for exit
import thread

from messages import MessageParser, DestinationPicker
from clienthandler import ClientHandler

class MessageClient():
    
    def __init__(self):
        self.server = "111.111.111.000"
        self.host = 'localhost';
        self.port = 7777;
        self.parser = MessageParser()
        self.handler = ClientHandler()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            self.ipaddr =  s.getsockname()[0]
            s.close()
        except socket.error:
            self.ipaddr = socket.gethostbyname(socket.gethostname())
 
    def create_udp_socket(self):
        # create dgram udp socket
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print 'Failed to create socket'
            sys.exit()
 
    def send_messages(self):
        while(1) :
            #client_list = DestinationPicker()
            #destination = client_list.pick_destination(client_list.test_avail_clients)
            
            source = self.ipaddr
            msg = self.handler.get_message(source)
            try :
                #Set the whole string
                self.s.sendto(msg, (self.host, self.port))
             
                #if payload == 'quit()':
                #    self.s.sendto(payload, (self.host, self.port))
                #    print 'quitting...'
                #    break

                # receive data from client (data, addr)
                d = self.s.recvfrom(1024)
                reply = d[0]
                addr = d[1]

                #get the payload
                response = self.parser.decode(reply)

                print 'Server reply : ' + reply
                print 'Response: ' + response["Payload"]
            
     
            except socket.error, msg:
                print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
                sys.exit()

    def get_messages():
        # for sending GET requests to the server
        source = self.ipaddr
        destination = self.server
        message = self.handler.get_request(source, destination)
        try:
            self.s.sendto(message, (self.host, self.port))
            message_list = []
            while(1):
                rec_msg = self.s.recvfrom(1024)
                data = rec_msg[0]
                addr = rec_msg[1]

                message_list.append(data)
                parsed_data = self.parser.decode(data)
                if parsed_data["Type"] == "EOM":
                    break

        except socket.error, message:
            print 'Error Code : ' + str(message[0]) + ' Message ' + message[1]

    def login(self):
        while(1) :
            username = raw_input('Enter your username: ')
            testip = raw_input('Enter your ip (test): ')
            msg = self.parser.encode("001","LOGIN",testip,"0.0.0.0",username)
            try :
                # Set the whole string
                self.s.sendto(msg, (self.host, self.port))

                # receive data from server (data, addr)
                d = self.s.recvfrom(1024)
                reply = d[0]
                addr = d[1]

                #get the payload
                response = self.parser.decode(reply)

                print 'Server reply : ' + reply
                print 'Response: ' + response["Payload"]

                if "successful" in response["Payload"]:
                    break
     
            except socket.error, msg:
                print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
                sys.exit()

def main():
    client = MessageClient()
    client.create_udp_socket()
    client.login()
    client.send_messages()

if __name__ == "__main__":
    main()
