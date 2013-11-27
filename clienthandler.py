'''
    3780 Networking Project
    Rio Lowry
'''

from messages import MessageParser

def get_ip(data):
    if data == "padme":
        return "142.66.140.119"
    if data == "dax":
        return "142.66.140.76"
    if data == "tuvok":
        return "142.66.140.77"
    if data == "solo"
        return "142.66.140.125"
    if data == "r2d2"
        return "142.66.140.124"
    return data

class ClientHandler():

    def __init__(self):
        self.parser = MessageParser()
        self.received_messages = {}
        self.resend_list = []
        self.sequence_no = 0
        self.get_seq_no = 0
        # need a window start and end for sendlist, can't send unless window has room

    def get_message(self, source):
        payload = raw_input('Enter message to send : ')
        destination = raw_input('Enter destination IP : ')
        destination = get_ip(destination)
        message_data = self.parser.encode(self.increment_seq_no(0),"SEND",source, destination, payload)
        self.resend_list.append(message_data)
        return message_data

    def increment_seq_no(self, type):
        if type == 0:
            seq_no = self.sequence_no
            self.sequence_no = (self.sequence_no + 1) % 1000
        elif type == 1:
            seq_no = self.get_seq_no
            self.get_seq_no = (self.get_seq_no + 1) % 1000
        return seq_no

    def parse(self, message_list):
        ack_list = []
        sorted_messages = sorted(message_list)
        for m in sorted_messages:
            
            message = self.parser.decode(m)

            if message["Type"] == "SEND":
                
                #acknowledge all messages of Type "SEND"
                ack_message = {}
                ack_message["Seq_No"] = message["Seq_No"] 
                ack_message["Type"] = "ACK"
                ack_message["Source"] = message["Destination"] 
                ack_message["Destination"] = message["Source"]
                ack_message["Payload"] = ""
                send_ack = self.parser.encode(ack_message["Seq_No"],
                        ack_message["Type"],
                        ack_message["Source"],
                        ack_message["Destination"],
                        ack_message["Payload"])
                ack_list.append(send_ack)

                if not self.seen_message(message):
                    self.save_message_seq_no(message)
                    print message["Source"] + ", says : " + message["Payload"]

            elif message["Type"] == "ACK":
                # message acknoledged we no longer want to resend it.
                self.remove_from_resend_list(message)

            elif message["Type"] == "REJ":
                #remove rejected messages
                self.remove_from_resend_list(message)
        
        return ack_list, self.resend_list

    def save_message_seq_no(self, message):
        
        # message is a dictionary, saves the sequence number
        save_string = message["Seq_No"] + message["Source"]
        self.received_messages[save_string] = True
        return True


    def seen_message(self, message):
        
        # Check to see if message is in _list
        check_string = message["Seq_No"] + message["Source"]
        if check_string in self.received_messages:
            return True
        else:
            return False

    def remove_from_resend_list(self, message):
        check_message = self.parser.encode(message["Seq_No"],
                        message["Type"],
                        message["Source"],
                        message["Destination"],
                        message["Payload"])
        # Don't resend these messages 
        if check_message in self.resend_list:
            self.resend_list(check_message)

    def get_request(self, source, destination):
        payload = ""
        message_data = self.parser.encode(self.increment_seq_no(1),"GET",source, destination, payload)
        return message_data
