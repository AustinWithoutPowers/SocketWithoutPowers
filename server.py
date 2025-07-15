import SocketWithoutPowers as SWP

SHUTDOWN_PHRASE = 'asdf'
PASSWORD = 'password1'
DEBUGGING = False

class SocketResponse:
    COMMAND_REQUEST = 'Please send command: '
    APPROVED = f'Approved. {COMMAND_REQUEST}'
    DECLINED = 'Declined'

def main():
    server_socket = SWP.ServerSocket(debug=DEBUGGING)
    server_socket.bind_and_listen()

    authenticated = False

    while True:
        client_socket = server_socket.accept()

        request = client_socket.receive()
        print(f'> {request}')
        if not authenticated:
            if request == PASSWORD:
                client_socket.send(SocketResponse.APPROVED)
                print('User authenticated')
                authenticated = True
            else:
                client_socket.send(SocketResponse.DECLINED)
        else:
            if request == SHUTDOWN_PHRASE:
                client_socket.shutdown()
                break
            client_socket.send(SocketResponse.COMMAND_REQUEST)
main()