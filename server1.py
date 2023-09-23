import threading
import socket
import rsa

public_key, private_key= rsa.newkeys(1024)
public_client=None

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("localhost",9999))
server.listen()

clients=[]
nicknames=[]

def broadcast(message):
    for client in clients:
        client.send(message)
        
def handle(client):
    while True:
        try:
            message=client.recv(1024)
            broadcast(message)
        except:
            index=client.index(client)
            clients.remove(client)
            client.close()
            nickname=nicknames[index]
            broadcast(f"{nickname} left the chat".encode('ascii'))
            nicknames.remove(nickname)
            break
        
def receive():
    while True:
        client, address=server.accept()
        print(f"Connected with {str(address)}")
        
        
        client.send("NICK".encode("ascii"))
        nickname=client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f'{nickname} JOINED THE CHAT'.encode('ascii'))
        client.send("CONNECTED TO SERVER!".encode('ascii'))

        thread=threading.Thread(target=handle, args=(client,))
        thread.start()

print("SERVER IS LISTENING..")
receive()