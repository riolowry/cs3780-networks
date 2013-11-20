'''
    3780 Networking Project server
    Rio Lowry 
'''
 
import socket
import sys

class MessageServer():

    def __init__(self, message_storage, message_handler, client_list):
        self.HOST = ''   # Symbolic name meaning all available interfaces
        self.PORT = 7777 # Arbitrary non-privileged port
        self.message_storage = message_storage
        self.message_handler = message_handler
        self.client_list = client_list
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
         
            if not data: 
                break

            if data == 'quit()':
                print 'quitting...'
                break

            # Send message to message handler
            reply,destination = self.message_handler.handle_message(message)
         
            print reply
            print destination
            print self.client_list.clients

            # Send a reply if necessary
            if reply and destination:
                self.s.sendto(reply,destination)

            self.parse_message(message[0])

    def parse_message(self, message):
        print "TODO ... The data is: " + message
     
    def close_socket(self):
        self.s.close()

