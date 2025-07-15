from core.socket_without_powers import ParentSocket, ServerSocket  

def manual_server_test():
    try:
        print('Browse to following URL to test:')
        print(f'http://{ParentSocket.DEFAULT_HOST}:{ParentSocket.DEFAULT_PORT}')
        test_sock = ServerSocket()
        test_sock.bind_and_listen()
        test_sock.accept()
    except Exception as e:
        print(f'Failed!: {e}')
    else:
        print('Passed!')

manual_server_test()