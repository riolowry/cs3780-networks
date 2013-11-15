import json
import heapq

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

    def remove_message(self, destination):
        # Remove and return message for destination with lowest seq no
        message = heapq.heappop(self.messages[destination])[1]
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
 
