'''
    3780 Networking Project server
    Rio Lowry 
'''
 
import socket
import sys
from messages import MessageParser

class MessageServer():

    def __init__(self):
        self.HOST = ''   # Symbolic name meaning all available interfaces
        self.PORT = 7777 # Arbitrary non-privileged port
        self.parser = MessageParser()
 
    def open_udp_socket(self):
        # Datagram (udp) socket
        try :
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print 'Socket created'
        except socket.error, msg :
            print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
 
 
    def bind_socket(self):
        # Bind socket to local host and port
        try:
            self.s.bind((self.HOST, self.PORT))
        except socket.error , msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
     
        print 'Socket bind complete'

    def listen(self):
        #now keep talking with the client
        while 1:
            # receive data from client (data, addr)
            d = self.s.recvfrom(1024)
            data = d[0]
            addr = d[1]
         
            if not data: 
                break

            if data == 'quit()':
                print 'quitting...'
                break
         
            test = self.parser.decode(data)
            print test

            reply = 'OK...' + data
         
            self.s.sendto(reply , addr)
            print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
            self.parse_message(data)

    def parse_message(self, message):
        print "TODO ... The data is: " + message
     
    def close_socket(self):
        self.s.close()

def main():
    myserver = MessageServer()
    myserver.open_udp_socket()
    myserver.bind_socket()
    myserver.listen()
    myserver.close_socket()

if __name__ == "__main__":
    main()
