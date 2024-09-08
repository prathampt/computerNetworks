import socket
import threading

class Client:
    def __init__(self, host, port, nickname):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.nickname = nickname
        self.running = True

    # Listening to Server and Sending Nickname
    def receive(self):
        while self.running:
            try:
                # Receive Message From Server
                # If 'NICK' Send Nickname
                message = self.client.recv(1024).decode('utf-8')
                if not message:
                    self.client.close()
                    break
                elif message == 'NICK':
                    self.client.send(nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                # Close Connection When Error
                print("An error occured!")
                self.client.close()
                break

    # Sending Messages To Server
    def write(self):
        while self.running:
            message = input('')
            if message.lower() == 'exit':
                self.client.send(f'Exiting form the chat. Exit code ##!0'.encode('utf-8'))
                self.client.close()
                self.running = False
                print("Disconnected from the server.")
            else:
                self.client.send(f"{message}".encode('utf-8'))

    def start(self):
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

        self.write_thread = threading.Thread(target=self.write)
        self.write_thread.start()


if __name__ == "__main__":
    nickname = input("Choose your nickname: ")
    c = Client('127.0.0.1', 55555, nickname)
    c.start()
