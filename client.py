'''
    3780 Networking Project
    Rio Lowry
'''
 
import socket   #for sockets
import sys  #for exit
from messages import MessageParser

class MessageClient():
    
    def __init__(self):
        self.host = 'localhost';
        self.port = 7777;
        self.parser = MessageParser()
 
    def create_udp_socket(self):
        # create dgram udp socket
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print 'Failed to create socket'
            sys.exit()
 
    def send_messages(self):
        while(1) :
            payload = raw_input('Enter message to send : ')
            msg = self.parser.encode("001","GET","255.255.255.255","255.255.255.255",payload)
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
         
                print 'Server reply : ' + reply
            
     
            except socket.error, msg:
                print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
                sys.exit()

def main():
    client = MessageClient()
    client.create_udp_socket()
    client.send_messages()

if __name__ == "__main__":
    main()
