import json
import heapq
import threading

class MessageStorage():

    def __init__(self):
        self.messages = self.read_from_file()
        for messagelist in self.messages.values():
            heapq.heapify(messagelist)

    def add_message(self, message):
        # Add a message with its destination as key
        destination = message["Destination"]
        if destination not in self.messages:
            self.messages[destination] = []
        heapq.heappush(self.messages[destination], [message["Seq_No"], message])

        self.write_to_file()

    def add_message_to_ip(self, message, ip):
        # Add a message with ip as key
        if ip not in self.messages:
            self.messages[ip] = []
        heapq.heappush(self.messages[ip], [message["Seq_No"], message])

        self.write_to_file()

    def remove_message(self, destination):
        # Remove and return message for destination with lowest seq no
        message = heapq.heappop(self.messages[destination])[1]
            
        self.write_to_file()

        return message

    def write_to_file(self):
        # Write messages to file
        try:
            with open('savedmessages.json','w') as f:
                json.dump(self.messages, f)
        except IOError, e:
            print "I/O error: %s" % e

    def read_from_file(self):
        # Read messages from file
        try:
            with open('savedmessages.json','r') as f:
                return json.load(f)
        except IOError, e:
            print "I/O error: %s" % e
            return {}

class ClientList():

    def __init__(self):
        self.active_clients = []
        self.clients = []
        self.timer = threading.Timer(600.0, self.reset_clients)
        self.timer.start()

    def add_client(self, ip):
        # Add a client to the list
        if ip not in self.clients:
            self.clients.append(ip)

    def add_active_client(self, ip):
        # Make client active
        if ip not in self.active_clients:
            self.active_clients.append(ip)

    def client_is_active(self, ip):
        # Return false if ip is not in clients
        return ip in self.clients

    def reset_clients(self):
        # Function to reset the list of clients to those active
        self.clients = self.active_clients
        self.active_clients = []
        print "CLIENTS RESET. Active clients: %s" % (self.clients, )
        self.timer = threading.Timer(600.0, self.reset_clients)
        self.timer.start()

    def stop_timer(self):
        self.timer.cancel()

        
