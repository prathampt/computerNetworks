import socket
import threading
from datetime import datetime

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []
        self.nicknames = []

    # Sending Messages To All Connected Clients
    def broadcast(self, message, selfClient):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for client in self.clients:
            if selfClient != client:
                client.send(f"[{timestamp}] {message}".encode('utf-8'))

    # Handling Messages From Clients
    def handle(self, client):
        while True:
            try:
                # Broadcasting Messages
                message = client.recv(1024)
                if not message:
                    raise Exception("Client disconnected")
                
                decoded_message = message.decode('utf-8')
            
                # Check for disconnect message
                if "Exiting form the chat. Exit code ##!0" in decoded_message:
                    index = self.clients.index(client)
                    nickname = self.nicknames[index]
                    self.clients.remove(client)
                    client.close()
                    self.nicknames.remove(nickname)
                    self.broadcast(f"{nickname} has left the chat!", None)
                    break

                index = self.clients.index(client)
                nickname = self.nicknames[index]
                formatted_message = f"{nickname}: {message.decode('utf-8')}"
                self.broadcast(formatted_message, client)
            except:
                # Removing And Closing Clients
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                print("{} disconnected!".format(self.nicknames[index]))
                nickname = self.nicknames[index]
                self.broadcast(f"{nickname} left the chat!", client)
                self.nicknames.remove(nickname)
                break
    # Receiving / Listening Function
    def start(self):
        print("The Server is started and listening on {}:{}".format(self.host, self.port))
        while True:
            # Accept Connection
            client, address = self.server.accept()
            print("Connected with {}".format(str(address)))

            # Request And Store Nickname
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
                
            # Print And Broadcast Nickname
            print("{} joined the server!".format(nickname))
            self.broadcast("{} joined!".format(nickname), client)
            client.send('Connected to server!'.encode('utf-8'))
            client.send(str(f"Connected Users: {len(self.nicknames)}\n" + "\n".join(self.nicknames)).encode('utf-8'))
            with threading.Lock():
                self.nicknames.append(nickname)
                self.clients.append(client)

            # Start Handling Thread For Client
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

if __name__ == "__main__":
    s = Server("127.0.0.1", 55555)
    s.start()