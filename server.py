import SocketWithoutPowers as SWP

def main():
    server_socket = SWP.ServerSocket(debug=True)
    server_socket.bind_and_listen()

    while True:
        # Accept connections from outside
        client_socket = server_socket.accept()

        request = client_socket.receive()
        if request is None:
            break
        elif request == 'password1':
            client_socket.send('Approved')
        else:
            client_socket.send('Declined')

main()