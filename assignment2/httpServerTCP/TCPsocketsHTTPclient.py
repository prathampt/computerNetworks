import socket

# Define the IP and port to connect to
HOST = '127.0.0.1'  # Server's IP address
PORT = 8080         # Server's port

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Send an HTTP GET request
request = "GET / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n"
client_socket.sendall(request.encode('utf-8'))

# Receive the response from the server
response = client_socket.recv(4096).decode('utf-8')
print(f'Response received:\n{response}')

# Close the connection
client_socket.close()
