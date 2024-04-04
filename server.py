import socket
import threading
import tkinter as tk

root = tk.Tk()

HOST = "127.0.0.1"
PORT = 8002 #0 to 65535
LISTENER_LIMIT = 10
active_clients = [] #all currently connected users

# function for listen for upcomming messages for client
def listen_for_messages(client, username):

    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        else:
            print(f"message sent from client {username} is empty")

# function to send message to single client
def send_message_to_client(client, message):

    client.sendall(message.encode())

# function to send any new message to all the client that are currently connected to the server
def send_messages_to_all(message):

    for user in active_clients:
        send_message_to_client(user[1], message)


# function to handle client
def client_handler(client):

    # server will listen to the client message that will contain the username
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username)).start()

# main function
def main():

    #Creating the server socket class object
    #AF_INET: we are going to useIPV4 addresse
    #SOCK_STREAM we are using TCP packet for communicatoion
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print(f"running the server on {HOST} {PORT}")

    #creating try catch block
    try:
        #provide the server with an address in the form of host IP and PORT
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")

    except:
        print(f"unable to bind the host {HOST} and port {PORT}")

    # set server limit
    server.listen(LISTENER_LIMIT)

    # this while loop will keep listening to client connections
    while 1:

        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__':
    main()
