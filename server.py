import threading
import socket

host = "127.0.0.1" #local host

port = 55555


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = [] 
nicknames = []

def braodcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            braodcast(message)
        except:
            index = client.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            t=str(nickname)+" Left the chat"
            braodcast(t.encode('ascii'))
            nicknames.remove(nickname)
            break


def recieve():
    while True:
        client, address = server.accept()
        print("Connected with "+str(address))
        client.send('nick'.encode('ascii'))
        nickname  = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(nickname+" is the nickname of the client")
        t=nickname+" joined the chat"
        braodcast(t.encode('ascii'))
        client.send("Connected to the server".encode('ascii'))

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()

print("Server is running....")
recieve()




