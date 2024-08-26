import sys
import socket

# Add this block of code at the top of your existing script
def resolve_hostname(hostname):
    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"{hostname} resolved to {ip_address}")
    except socket.gaierror:
        print(f"Error: Cannot resolve hostname '{hostname}'")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        hostname = sys.argv[1]
        resolve_hostname(hostname)
    elif len(sys.argv) > 2:
        print("Error: Too many arguments provided.")
        sys.exit(1)
    else:
        print("Error: No hostname provided.")
        sys.exit(1)
    
