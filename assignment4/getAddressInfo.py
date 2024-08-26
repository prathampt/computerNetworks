import socket

def resolve_domain(domain_name):
    try:
        results = socket.getaddrinfo(domain_name, None)
        print(f"IP addresses for {domain_name}:")
        for result in results:
            ip_address = result[4][0]
            address_family = result[0]
            socket_type = result[1]
            
            # Determine the address family (IPv4 or IPv6)
            if address_family == socket.AF_INET:
                address_type = "IPv4"
            elif address_family == socket.AF_INET6:
                address_type = "IPv6"
            else:
                address_type = "Unknown"
            
            # Determine the socket type (Stream/TCP, Datagram/UDP, or Raw)
            if socket_type == socket.SOCK_STREAM:
                socket_type_str = "Stream (TCP)"
            elif socket_type == socket.SOCK_DGRAM:
                socket_type_str = "Datagram (UDP)"
            elif socket_type == socket.SOCK_RAW:
                socket_type_str = "Raw"
            else:
                socket_type_str = "Unknown"

            print(f"IP address: {ip_address} || Address type: {address_type} || Socket type: {socket_type_str}")
    except socket.gaierror:
        print(f"Error: Cannot resolve domain name '{domain_name}'")

if __name__ == "__main__":
    domain_name = input("Enter a domain name: ")
    resolve_domain(domain_name)
