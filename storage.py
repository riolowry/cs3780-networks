class MessageStorage():

    def __init__(self):
        self.messages = {}

    def add_message(self, message):
        # Add a message with its destination as key
        destination = message["Destination"]
        if destination not in self.messages:
            self.messages[destination] = []
        else:
            self.messages[destination].append(message)

        print self.messages[destination]
