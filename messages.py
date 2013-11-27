'''
    3780 Networking Project message parser
    Rio Lowry 
'''

import re

class MessageParser():

    def decode(self, data):
        #validate data
        check = r'\d+(GET|SEND|ACK|EOM)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}#\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.*'
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
        m_type = re.search(r'(GET|SEND|ACK|EOM)',data)
        addr = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',data)
        payl = data.find(addr[1])+len(addr[1])
        
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
        parsed_message = self.message_parser.decode(message[0])   

        if parsed_message["Type"] == "SEND" or parsed_message["Type"] == "ACK":
            # Store SEND and ACK messages
            self.message_storage.add_message(parsed_message)
        elif parsed_message["Type"] == "GET":
            # Send all user's messages upon a GET request, ending with an EOM
            source = parsed_message["Source"]
            while self.message_storage.messages[source]:
                # Loop until the server sends an EOM type message

                msg = self.message_storage.messages[source][0][1]
                encoded_message = self.message_parser.encode(msg["Seq_No"], msg["Type"], msg["Source"], msg["Destination"], msg["Payload"])
                print encoded_message
                self.server.send_message(encoded_message, message[1])
                print message[1]

                self.message_storage.remove_message(source)

            EOM = self.message_parser.encode(parsed_message["Seq_No"], "EOM", source, source, "EOM")
            self.server.send_message(EOM, message[1])

        return
            
def main():
    test = DestinationPicker()
    clients = test.test_avail_clients
    destination = test.pick_destination(clients)
    print destination

if __name__ == "__main__":
    main()
