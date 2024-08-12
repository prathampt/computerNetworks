import socket

# Define the IP and port for the server to listen on
HOST = '127.0.0.1'  # Localhost
PORT = 8080         # Non-privileged port

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections (up to 5 simultaneous connections)
    server_socket.listen(5) # 5 indicates the number of queued connections is 5...
    print(f'Server is listening on {HOST}:{PORT}')

    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()
        print(f'Connected by {client_address}')
        
        # Receive the request from the client
        request = client_socket.recv(1024).decode('utf-8') # Reads max upto 1024 bytes from the client
        print(f'Request received:\n{request}')

        # Prepare a simple HTTP response
        try:
            with open("index.html", 'r') as f:
                response = f"""HTTP/1.1 200 OK
    Content-Type: text/html

    {f.read()}"""
        except FileNotFoundError:
            response = response = """HTTP/1.1 200 OK
Content-Type: text/html

<html>
    <body>
        <h1>Hello World!</h1>
    </body>
</html>"""

        # Send the HTTP response to the client
        client_socket.sendall(response.encode('utf-8'))
        
        # Close the connection with the client
        client_socket.close()

