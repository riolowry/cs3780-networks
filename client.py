'''
    3780 Networking Project
    Rio Lowry
'''
 
import socket   #for sockets
import sys  #for exit
import thread

from messages import MessageParser, DestinationPicker
from clienthandler import *


class MessageClient():
    
    def __init__(self):
        self.server = raw_input('Enter server IPaddress: ')
        self.server = get_ip(self.server)         
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
        #while(1) :
        #    #client_list = DestinationPicker()
        #    #destination = client_list.pick_destination(client_list.test_avail_clients)
            
        source = self.ipaddr
        #    #self.get_messages()
        msg = self.handler.get_message(source)
        try :
            #    #Set the whole string
            self.s.sendto(msg, (self.server, self.port))
             
            #    #if payload == 'quit()':
            #    #    self.s.sendto(payload, (self.host, self.port))
            #    #    print 'quitting...'
            #    #    break

            #   # receive data from client (data, addr)
            #    #d = self.s.recvfrom(1024)
            #    #reply = d[0]
            #    #addr = d[1]

            #    #get the payload
            #    #response = self.parser.decode(reply)

            #   #print 'Server reply : ' + reply
            #    #print 'Response: ' + response["Payload"]
            
     
        except socket.error, msg:
            print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

    def get_messages(self):
        # for sending GET requests to the server
        source = self.ipaddr
        destination = self.server
        message = self.handler.get_request(source, destination)
        try:
            self.s.sendto(message, (self.server, self.port))
            message_list = []
            while(1):
                rec_msg = self.s.recvfrom(1024)
                data = rec_msg[0]
                addr = rec_msg[1]

                message_list.append(data)
                parsed_data = self.parser.decode(data)
                if parsed_data["Type"] == "EOM":
                    print "EOM recieved"
                    break

            ack_list, resend_list = self.handler.parse(message_list)

            for msg in ack_list:
                try:
                    self.s.sendto(msg, (self.server, self.port))
                except:
                    continue

            for msg in resend_list:
                try:
                    self.s.sendto(msg, (self.server, self.port))
                except:
                    continue

        except socket.error, message:
            print 'Error Code : ' + str(message[0]) + ' Message ' + message[1]

    def login(self):
        username = "login from " + str(self.ipaddr) #raw_input('Enter your username: ')
        msg = self.parser.encode("001","LOGIN",str(self.server),"0.0.0.0",username)
        try :
            self.s.sendto(msg, (self.server, self.port))
     
        except socket.error, msg:
            print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
    
    def kill_server(self):
        msg = ""
        try :
            self.s.sendto(msg, (self.server, self.port))
     
        except socket.error, msg:
            print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()


def main():
    client = MessageClient()
    client.create_udp_socket()
    client.login()
    while(1):
        cmd = raw_input('"GET", "SEND", or "Quit" ? ')
        if cmd == "SEND":
            client.send_messages()
        elif cmd == "GET":
            client.get_messages()
        elif cmd == "Quit":
            break
        elif cmd == "QuitServer":
            client.kill_server()


if __name__ == "__main__":
    main()
