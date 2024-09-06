import socket
import threading

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
        for client in self.clients:
            if selfClient != client:
                client.send(message)

    # Handling Messages From Clients
    def handle(self, client):
        while True:
            try:
                # Broadcasting Messages
                message = client.recv(1024)
                self.broadcast(message, client)
            except:
                # Removing And Closing Clients
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast('{} left!'.format(nickname).encode('utf-8'), client)
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
            self.clients.append(client)

            # Print And Broadcast Nickname
            print("{} joined the server!".format(nickname))
            self.broadcast("{} joined!".format(nickname).encode('utf-8'), client)
            client.send('Connected to server!'.encode('utf-8'))
            client.send(str(f"Connected Users: {len(self.nicknames)}\n" + "\n".join(self.nicknames)).encode('utf-8'))
            self.nicknames.append(nickname)

            # Start Handling Thread For Client
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()


s = Server("127.0.0.1", 55555)
s.start()