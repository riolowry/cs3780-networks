import json

class MessageStorage():

    def __init__(self):
        self.messages = self.read_from_file()

    def add_message(self, message):
        # Add a message with its destination as key
        destination = message["Destination"]
        if destination not in self.messages:
            self.messages[destination] = []
        self.messages[destination].append(message)

        self.write_to_file()

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
 
