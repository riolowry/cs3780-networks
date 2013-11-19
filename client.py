'''
    3780 Networking Project
    Rio Lowry
'''
 
import socket   #for sockets
import sys  #for exit
from messages import MessageParser, DestinationPicker

class MessageClient():
    
    def __init__(self):
        self.host = 'localhost';
        self.port = 7777;
        self.parser = MessageParser()
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
            client_list = DestinationPicker()
            destination = client_list.pick_destination(client_list.test_avail_clients)
            payload = raw_input('Enter message to send : ')
            source = self.ipaddr
            msg = self.parser.encode("001","GET",source, destination, payload)
            try :
                #Set the whole string
                self.s.sendto(msg, (self.host, self.port))
             
                if payload == 'quit()':
                    self.s.sendto(payload, (self.host, self.port))
                    print 'quitting...'
                    break

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
