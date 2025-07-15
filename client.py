import SocketWithoutPowers as SWP

DEBUGGING = False

def main():
    message = ''
    for i in range(1024):
        message += str(i)

    client_chat = SWP.ChatClient(debug=DEBUGGING)
    client_chat.chat_loop(end_command='qwer')
    
    
main()