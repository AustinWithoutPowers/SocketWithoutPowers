import SocketWithoutPowers as SWP

def main():
    message = ''
    for i in range(1024):
        message += str(i)

    client_chat = SWP.ChatClient()
    client_chat.chat_loop()
    
    
main()