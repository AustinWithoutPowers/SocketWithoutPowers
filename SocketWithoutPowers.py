import socket

class ParentSocket:
    '''
    Creates a custom, parent socket class.

    Utilised by SocketWithoutPowers.ClientSocket and SocketWithoutPowers.ServerSocket.
    '''
    KB = 1024
    def __init__(self, sock = None, debug = False):
        '''
        Initialises a SocketWithoutPowers.ParentSocket object.

        Takes an optional socket.socket object, and an optional boolean for debugging.
        '''
        self.debug_enabled = debug # Need to do this first

        if sock is None:
            self.debug('Creating default socket.')
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.debug('Creating provided socket.')
            self.sock = sock
    
    def debug(self, message):
        '''
        Prints a debug message if the debug flag is set.

        Takes a string object for the message to (maybe) print.
        '''
        if self.debug_enabled:
            print('DEBUG:', message)

class ClientSocket(ParentSocket):
    '''
    Creates a custom, client socket. Extends SocketWithoutPowers.ParentSocket.
    '''
    def __init__(self, sock = None, debug = False):
        '''
        Initialises a SocketWithoutPowers.ClientSocket object.
        
        Takes an optional socket.socket object for the socket,
        and an optional boolean for debugging.
        '''
        self = super().__init__(sock, debug)

    def connect(self, hostname, port):
        '''
        Connects to a remote host and port.

        Takes two string objects for the server host and server port to connect to.
        '''
        self.sock.connect((hostname, port))
        self.debug('Connected!')
    
    def send(self, msg):
        '''
        Sends a message to the connected server, using a KB sized buffer.

        This then triggers socket.shutdown() on the client socket, but not socket.close().

        Takes a string object for the message.
        '''
        encoded_msg = msg.encode()
        self.debug('Beginning to send.')
        total_sent = 0
        while total_sent < len(encoded_msg):
            chunk = encoded_msg[total_sent:min(
                    total_sent + self.KB, len(encoded_msg))]
            sent = self.sock.send(chunk)
            self.debug('Chunk sent!')
            if sent == 0:
                raise RuntimeError('Socket connection broken.')
            total_sent += sent
        self.shutdown()
        self.debug('All chunks sent!')

    def receive(self):
        '''
        Returns a string object, being the message from a client server, using a KB sized buffer.
        '''
        self.debug('Beginning to receive.')
        chunks = []
        bytes_received = 0
        # Loop connection until message fully received
        while True:
            chunk = self.sock.recv(self.KB)
            # Connection closed or message fully received
            if chunk == b'':
                self.debug('EOF!')
                break

            self.debug('Non-ending chunk received!')
            # Add the chunk and increase byte count
            chunks.append(chunk)
            bytes_received += len(chunk)
        return chunks[0].decode()
    
    def shutdown(self):
        '''
        Executes socket.shutdown(1) on the saved socket.
        '''
        self.sock.shutdown(1)
    
    def close(self):
        '''
        Executes socket.close() on the saved socket.
        '''
        self.sock.close()

    def end(self):
        '''
        Executes both socket.shutdown(1) and socket.close() in a single function.
        '''
        self.shutdown()
        self.close()

class ServerSocket(ParentSocket):
    '''
    Creates a custom, server socket. Extends SocketWithoutPowers.ParentSocket.
    '''

    # Not sure if I like this instead of variables assigned to self.
    DEFAULT_HOST = socket.gethostname()
    DEFAULT_PORT = 80
    DEFAULT_LISTEN_COUNT = 5

    def __init__(self, shutdown_phrase = 'SHUTDOWN',
                 sock = None, debug = False):
        '''
        Initialises a SocketWithoutPowers.ServerSocket object.
        
        Takes an optional string object for the shutdown phrase,
        socket.socket object for the socket,
        and an optional boolean for debugging.
        '''
        self = super().__init__(sock, debug)
        self.__shutdown_phrase = shutdown_phrase

    def bind(self, hostname, server_port):
        '''
        Executes socket.bind((hostname, server_port)).
        
        Takes two string objects, for the server host and the server port.
        '''
        self.sock.bind((hostname, server_port))
        self.debug('Bound!')
    
    def listen(self, count):
        '''
        Executes socket.listen(count).
        
        Takes an int object, for the maximum number of connections
        to accept before dropping new messages.
        '''
        self.sock.listen(count)
        self.debug('Listening!')
    
    # Creating this to quickly spin up a socket
    def bind_and_listen(self):
        '''
        Executes SocketWithoutPowers.ServerSocket.bind(hostname, server port) and
        SocketWithoutPowers.ServerPort.listen(count) with \"default\" values.

        Mostly used for testing, but can be used for \"default\" setups.
        '''
        self.bind(self.DEFAULT_HOST, self.DEFAULT_PORT)
        self.listen(self.DEFAULT_LISTEN_COUNT)
    
    def accept(self):
        '''
        Executes socket.accept() and returns any incoming
        SocketWithoutPowers.ClientSocket objects.
        '''
        self.debug('Accepting!')
        return ClientSocket(self.sock.accept()[0], self.debug)

class ChatClient:
    '''
    Creates a chat client to communicate with a SocketWithoutPowers.ChatServer object.
    '''
    DEFAULT_HOST = socket.gethostname()
    DEFAULT_PORT = 80

    # Cannot think of a good way to do this...
    OK = 0
    NO_RESP = 1
    AUTH_ERROR = 2

    def __init__(self, server_host = DEFAULT_HOST,
                 server_port = DEFAULT_PORT):
        '''
        Initialises a SocketWithoutPowers.ChatClient object.
        
        Takes an optional string object for a server host,
        and an optional int object for a server port.
        '''
        self.__server_host = server_host
        self.__server_port = server_port

    def send_message(self, message):
        '''
        Sends a message to the server and returns a string object for the response.
        
        Takes a string object, for the message.
        '''
        sock = ClientSocket()
        sock.connect(self.__server_host,
                             self.__server_port)
        sock.send(message)
        response = sock.receive()
        sock.end()
        if response is None:
            return (self.NO_RESP, None)
        return (self.OK, response)
    
    def chat_loop(self, end_command = ''):
        '''
        Starts a "chat loop", which will send messages to the server until
        an empty string (or provided string) is input.

        Takes a string object, for a custom end command.
        '''
        while True:
            message = input()
            if message == end_command:
                break
            response = self.send_message(message)
            if response[0] == self.OK:
                print(response[1])
            else:
                raise RuntimeError(f'Error code {response[0]}.')