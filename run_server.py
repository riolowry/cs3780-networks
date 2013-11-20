from server import MessageServer
from storage import MessageStorage, ClientList
from messages import MessageParser, ServerMessageHandler


def main():
    storage = MessageStorage()
    parser = MessageParser()
    message_handler = ServerMessageHandler(parser)
    client_list = ClientList()
   
    myserver = MessageServer(storage, message_handler, client_list)
    myserver.open_udp_socket()
    myserver.bind_socket()
    myserver.listen()
    myserver.close_socket()

if __name__ == "__main__":
    main()
