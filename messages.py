'''
    3780 Networking Project server
    @author Rio Lowry, Lezar de Guzmann 
'''

import re

class MessageParser():

    def decode(self, data):
        #validate data
        check = r'\d+(GET|SEND|ACK|EOM|LOGIN|REJ)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}#\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}#.*'
        valid = re.match(check, data)
        message = {}
        
        if not valid:
            message["Seq_No"] =  "xxx"
            message["Type"] =  None
            message["Source"] = 0 
            message["Destination"] = 0
            message["Payload"] = "Bad Message!"
            return message

        #use re to parser the data
        seq = re.match(r'\d+',data)
        m_type = re.search(r'(GET|SEND|ACK|EOM|LOGIN|REJ)',data)
        addr = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',data)
        payl = data.find('#')+len(addr[1])+2
        
        message["Seq_No"] =  seq.group()
        message["Type"] =  m_type.group()
        message["Source"] = addr[0] 
        message["Destination"] = addr[1]
        message["Payload"] = data[payl:]
        #print message
        return message

    def encode(self, sequence_no, message_type, source, destination, payload):
        data = []
        data.append(str(sequence_no))
        data.append(str(message_type))
        data.append(str(source))
        data.append('#')
        data.append(str(destination))
        data.append('#')
        data.append(str(payload))
        message = ''.join(data)
        return message

class DestinationPicker():

    def __init__(self):
        self.test_avail_clients = {}
        user1 = "Bob"
        self.test_avail_clients[user1] = "128.555.2.1"
        user2 = "Sally"
        self.test_avail_clients[user2] = "196.28.56.140"
        
    def pick_destination(self, available_clients):
        print "The available hosts are: "
        for key, value in available_clients.iteritems() :
            print "User:" + key +" IP: " + value
        destination = raw_input ('Please type a username to send to: ')
        for key, value in available_clients.iteritems() :
            if key == destination:
                return value
        return "0.0.0.0"

class ServerMessageHandler():

    def __init__(self, message_parser, message_storage):
        self.message_parser = message_parser
        self.message_storage = message_storage

    def bind_server(self, server):
        # Bind self to a specific server object
        self.server = server

    def handle_message(self, message):
        # Decode and handle message return the reply string and its destination address
        print self.message_storage.messages
        parsed_message = self.message_parser.decode(message[0])
        source = parsed_message["Source"]
        
        self.server.clientlist.add_active_client(source)

        if parsed_message["Type"] == "SEND" or parsed_message["Type"] == "ACK":
            # Handle SEND AND ACK
            if self.server.clientlist.client_is_active(parsed_message["Destination"]):
                # Store SEND and ACK messages if destination is active
                self.message_storage.add_message(parsed_message)
            else:
                # If the recipient is inactive, discard ACK, and send rejected messages back to source
                if parsed_message["Type"] != "ACK":
                    encoded_message = self.message_parser.encode(parsed_message["Seq_No"], "REJ", parsed_message["Source"], parsed_message["Destination"], parsed_message["Payload"])
                    decoded_message = self.message_parser.decode(encoded_message)
                    self.message_storage.add_message_to_ip(decoded_message, source)

        elif parsed_message["Type"] == "GET":
            # Send all user's messages upon a GET request, ending with an EOM
            
            if source in self.message_storage.messages:
                while self.message_storage.messages[source]:
                    # Loop until the server sends an EOM type message
                    
                    msg = self.message_storage.messages[source][0][1]
                    encoded_message = self.message_parser.encode(msg["Seq_No"], msg["Type"], msg["Source"], msg["Destination"], msg["Payload"])
                    self.server.send_message(encoded_message, message[1])
                    self.message_storage.remove_message(source)

            EOM = self.message_parser.encode(parsed_message["Seq_No"], "EOM", source, source, "EOM")
            self.server.send_message(EOM, message[1])
        elif parsed_message["Type"] == "LOGIN":
            # Add client to the list of current clients and message storage
            self.server.clientlist.add_client(source)
            self.message_storage.add_client(source)

        return
            
def main():
    parser = MessageParser()

if __name__ == "__main__":
    main()
