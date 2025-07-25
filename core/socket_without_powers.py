import socket

class ParentSocket:
    '''
    Creates a custom, parent socket class.
    Utilised by ClientSocket and ServerSocket.
    '''
    KB = 1024
    DEFAULT_HOST = socket.gethostname()
    DEFAULT_PORT = 80
    
    def __init__(self, sock = None, debug = False):
        '''
        Initialises a SocketWithoutPowers.ParentSocket object.
        Takes an optional socket.socket object,
        and an optional boolean for debugging.
        '''
        self._debug_enabled = debug

        if sock is None:
            self._debug('Creating default socket.')
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self._debug('Creating passed socket.')
            self._sock = sock
    
    def _debug(self, message):
        '''
        Prints a debug message on the console if debug is enabled.
        '''
        if self._debug_enabled:
            print('DEBUG:', message)
    
    def close(self):
        '''
        Calls socket.close() on the saved socket.
        '''
        self._sock.close()

class ClientSocket(ParentSocket):
    '''
    Creates a custom, client socket. Extends ParentSocket.
    '''
    def __init__(self, sock = None, debug = False):
        '''
        Initialises a ClientSocket warpper object.
        '''
        super().__init__(sock, debug)

    def connect(self, hostname, port):
        '''
        Connects to a remote host and port using the base socket class.
        '''
        self._sock.connect((hostname, port))
        self._debug('Connected!')
    
    def send(self, msg):
        '''
        Sends a message to the connected server, using a KB sized buffer.
        This then triggers socket.shutdown() on the client socket,
        but not socket.close().
        '''
        encoded_msg = msg.encode()
        self._debug('Ready to send.')
        total_sent = 0
        while total_sent < len(encoded_msg):
            chunk = encoded_msg[total_sent:min(
                    total_sent + self.KB, len(encoded_msg))]
            sent = self._sock.send(chunk)
            self._debug('Chunk sent!')
            if sent == 0:
                raise RuntimeError('Socket connection broken.')
            total_sent += sent
        self.shutdown()
        self._debug('All chunks sent!')

    def receive(self):
        '''
        Returns a string object, message is from a client server,
        using a KB sized buffer.
        '''
        self._debug('Beginning to receive.')
        chunks = []
        bytes_received = 0
        while True:
            chunk = self._sock.recv(self.KB)
            if chunk == b'':
                self._debug('EOF!')
                break

            self._debug('Non-ending chunk received!')
            chunks.append(chunk)
            bytes_received += len(chunk)
        if chunks == []:
            return ''
        return chunks[0].decode()
    
    def shutdown(self):
        '''
        Calls socket.shutdown(1) on the saved socket.
        '''
        self._sock.shutdown(1)

    def end(self):
        '''
        Executes both socket.shutdown(1) and socket.close() in a single
        function.
        '''
        self.shutdown()
        self.close() # In parent class

class ServerSocket(ParentSocket):
    '''
    Creates a custom, server socket. Extends ParentSocket.
    '''
    DEFAULT_LISTEN_COUNT = 5

    def __init__(self, sock = None, debug = False):
        '''
        Initialises a ServerSocket warpper object.
        '''
        super().__init__(sock, debug)

    def bind(self, hostname, server_port):
        '''
        Executes socket.bind((hostname, server_port)).
        '''
        self._sock.bind((hostname, server_port))
        self._debug('Bound!')
    
    def listen(self, count):
        '''
        Executes socket.listen(count).
        '''
        self._sock.listen(count)
        self._debug('Listening!')
    
    # Creating this to quickly spin up a socket.
    def bind_and_listen(self):
        '''
        Executes self.bind(hostname, server port) and self.listen(count) with
        "default" values.

        Mostly used for testing, but can be used for "default" setups.
        '''
        self.bind(self.DEFAULT_HOST, self.DEFAULT_PORT)
        self.listen(self.DEFAULT_LISTEN_COUNT)
    
    def accept(self):
        '''
        Executes socket.accept() and returns a ClientSocket wrapper around the
        socket object.
        '''
        self._debug('Accepting!')
        return ClientSocket(self._sock.accept()[0], self._debug_enabled)

class ChatClient(ParentSocket):
    '''
    Creates a chat client to communicate with a ChatServer object.
    '''
    def __init__(self, sock = None, debug = False):
        '''
        Initialises a ChatClient object. Extends ParentSocket.
        '''
        super().__init__(sock, debug)
        self.__server_host = ParentSocket.DEFAULT_HOST
        self.__server_port = ParentSocket.DEFAULT_PORT

    def send_message(self, message):
        '''
        Sends a message to the server and returns a string object for the
        response.
        '''
        sock = ClientSocket()
        sock.connect(self.__server_host,
            self.__server_port)
        sock.send(message)
        response = sock.receive()
        sock.end()
        if response is None:
            return ''
        return response
    
    def chat_loop(self, end_command = ''):
        '''
        Starts a "chat loop", which will send messages to the server until
        the server sends back an empty string due to shutdown.
        '''
        while True:
            message = input()
            response = self.send_message(message)
            print(f'> {response}')
            if response == '':
                self._debug('End command received, exiting chat.')
                break