'''
    3780 Networking Project
    Rio Lowry
'''

from messages import MessageParser
import re

def get_ip(data):
    """simple helper function, translates IP addresses for a few lab machines"""
    if data == "padme":
        return "142.66.140.119"
    if data == "dax":
        return "142.66.140.76"
    if data == "tuvok":
        return "142.66.140.77"
    if data == "solo":
        return "142.66.140.125"
    if data == "r2d2":
        return "142.66.140.124"
    if data == "quigon":
        return "142.66.140.123"
    if data == "vader":
        return "142.66.56.232"
    if data == "orator":
        return "142.66.56.95"
    return data

class ClientHandler():

    def __init__(self):
        self.parser = MessageParser()
        self.received_messages = {}
        self.resend_list = {}
        self.sequence_no = 0
        self.get_seq_no = 0
        # need a window start and end for sendlist, can't send unless window has room

    def get_message(self, source):
        """queries user and creates new SEND message"""
        payload = raw_input('Enter message to send : ')
        while 1:
            destination = raw_input('Enter destination IP : ')
            destination = get_ip(destination)
            check = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
            valid = re.match(check, destination)
            if not valid:
                print "Ill-formed IP address. Please re-enter."
            else:
                break
        seq_no = self.increment_seq_no(0)
        message_data = self.parser.encode(seq_no,"SEND",source, destination, payload)
        key = str(seq_no) + str(destination)
        self.resend_list[key] = message_data
        #print "DEBUG: resend list:"
        #print "RESEND_LIST:" + str(self.resend_list)
        return message_data

    def increment_seq_no(self, type):
        """handles counter incrementation"""
        if type == 0:
            seq_no = self.sequence_no
            self.sequence_no = (self.sequence_no + 1) % 1000
        elif type == 1:
            seq_no = self.get_seq_no
            self.get_seq_no = (self.get_seq_no + 1) % 1000
        return seq_no

    def parse(self, message_list):
        """Parses and ACKs mesages, prints new messages and removed ACKed or REJected messages"""
        ack_list = []
        sorted_messages = sorted(message_list)
        for m in sorted_messages:

            #print "DEBUG: the message is: '" + m + "'."
            
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
                    print message["Source"] + ", says: " + message["Payload"]

            elif message["Type"] == "ACK":
                # message acknoledged we no longer want to resend it.
                self.remove_from_resend_list(message)

            elif message["Type"] == "REJ":
                message["Type"] = "SEND"
                #reverse destination and source order since server only echoes the message
                destination = message["Destination"]
                message["Destination"] = message["Source"]
                message["Source"] = destination
                #remove rejected messages
                self.remove_from_resend_list(message)
        
        return ack_list, self.resend_list

    def save_message_seq_no(self, message):
        """stores the sequence number and source of messages we have seen"""
        # message is a dictionary, saves the sequence number
        save_string = message["Seq_No"] + message["Source"]
        self.received_messages[save_string] = True
        return True


    def seen_message(self, message):
        """Does a quick check to see if this is a new or old message"""
        # Check to see if message is in recieved messages list
        check_string = message["Seq_No"] + message["Source"]
        if check_string in self.received_messages:
            #print "DEBUG: !!! we have seen message# " + message["Seq_No"] + " from " + message["Source"]
            return True
        else:
            #print "DEBUG: New message# " + message["Seq_No"] + " from " + message["Source"] + ":"
            return False

    def remove_from_resend_list(self, message):
        """removes messages from the resend list when they are ACKed or REJected"""
        #be able to remove message based on Seq No and IP only
        #key = message["Seq_No"] + message["Destination"]
        key = message["Seq_No"] + message["Source"]
        '''check_message = self.parser.encode(message["Seq_No"],
                        message["Type"],
                        message["Source"],
                        message["Destination"],
                        message["Payload"])'''
        # Don't resend these messages 
        try:
            #print "DEBUG:resend list, before remove:"
            #print "DEBUG: " + str(self.resend_list)
            del self.resend_list[key]
            #print "DEBUG:resend list, after remove:"
            #print "DEBUG: " + str(self.resend_list)
            ##print "DEBUG: *** message:'" + key + "' removed from resend list! ***"
        except KeyError:
            print key + " is not in resend list"

    def get_request(self, source, destination):
        """creates a GET request and returns the message string"""
        payload = ""
        message_data = self.parser.encode(self.increment_seq_no(1),"GET",source, destination, payload)
        return message_data
