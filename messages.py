'''
    3780 Networking Project message parser
    Rio Lowry 
'''

class MessageParser():

    def decode(self, data):
        message = {}
        message["Seq_No"] = data[:3]
        message["Type"] = data[3:6]
        message["Source"] = data[6:22]
        message["Destination"] = data[22:32]
        message["Payload"] = data[32:]
        return message

    def encode(self, sequence_no, message_type, source, destination, payload):
        data = []
        data.append(sequence_no)
        data.append(message_type)
        data.append(source)
        data.append(destination)
        data.append(payload)
        message = ''.join(data)
        return message
