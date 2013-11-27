'''
    3780 Networking Project server
    Rio Lowry 
'''
 
import socket
import sys

class MessageServer():

    def __init__(self, message_handler):
        self.HOST = ''   # Symbolic name meaning all available interfaces
        self.PORT = 7777 # Arbitrary non-privileged port
        self.message_handler = message_handler
        self.message_handler.bind_server(self)
 
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
            # receive message from client
            message = self.s.recvfrom(1024)

            data = message[0]
            addr = message[1]

            print message[0]
         
            if not data: 
                break

            if data == 'quit()':
                print 'quitting...'
                break

            # Send message to message handler
            self.message_handler.handle_message(message)

    def send_message(self, message, destination):
        # Send a message to a distination
        self.s.sendto(message, destination)

    def close_socket(self):
        self.s.close()

