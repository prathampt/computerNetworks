import socket
import json
import os

# Supported DNS query types
QUESTION_TYPES = {
    b"\x00\x01": "a"
}

# Holds the DNS zones
ZONES = {}

# Google DNS Resolver
GOOGLE_DNS = "8.8.8.8"
GOOGLE_PORT = 53

def load_zones():
    """ Load all zones from the 'Zones' directory """
    global ZONES
    zones_path = "Zones"
    json_zone = {}
    
    try:
        files = os.listdir(zones_path)
    except FileNotFoundError:
        zones_path = "..\\Zones"
        files = os.listdir(zones_path)
        
    for zone_file in os.listdir(zones_path):
        with open(os.path.join(zones_path, zone_file), "r") as f:
            data = json.load(f)
            zone_name = data["$origin"]
            json_zone[zone_name] = data
    
    return json_zone

ZONES = load_zones()

def get_zone(domain):
    """ Retrieve the zone for a given domain """
    global ZONES
    zone_name = ".".join(domain)
    return ZONES.get(zone_name)

class DNSGen:
    def __init__(self, data):
        self.data = data
        self.QR = "1"  # Response
        self.AA = "1"  # Authoritative Answer
        self.TC = "0"  # Truncated
        self.RD = "0"  # Recursion Desired
        self.RA = "0"  # Recursion Available
        self.Z = "000"  # Reserved
        self.RCODE = "0000"  # Response code
        self.QDCOUNT = b"\x00\x01"  # Number of questions
        self.NSCOUNT = b"\x00\x00"  # Number of authority records
        self.ARCOUNT = b"\x00\x00"  # Number of additional records
        self.format_error = 0  # Indicates if there was a format error
        self.domain = ""

    def _get_transaction_id(self):
        return self.data[0:2]

    def _get_opcode(self):
        byte1 = self.data[2:3]
        opcode = ""
        for bit in range(1, 5):
            opcode += str(ord(byte1) & (1 << bit))
        return opcode

    def _generate_flags(self):
        flags1 = int(self.QR + self._get_opcode() + self.AA + self.TC + self.RD, 2).to_bytes(1, byteorder="big")
        flags2 = int(self.RA + self.Z + self.RCODE, 2).to_bytes(1, byteorder="big")
        return flags1 + flags2

    def _get_question_domain_type(self, data):
        state = 0
        expected_length = 0
        domain_string = ""
        domain_parts = []
        question_type = None
        x = 0
        y = 0
        
        try:
            for byte in data:
                if state == 1:
                    if byte != 0:
                        domain_string += chr(byte)
                    x += 1
                    if x == expected_length:
                        domain_parts.append(domain_string)
                        domain_string = ""
                        state = 0
                    if byte == 0:
                        domain_parts.append(domain_string)
                        break
                else:
                    state = 1
                    expected_length = byte
                y += 1
            question_type = data[y:y+2]
            self.domain = ".".join(domain_parts)
        except IndexError:
            self.format_error = 1
        finally:
            return domain_parts, question_type

    def _get_records(self, data):
        domain, question_type = self._get_question_domain_type(data)
        if question_type is None or len(domain) == 0:
            return {}, "", ""
        qt = QUESTION_TYPES.get(question_type, "a")
        zone = get_zone(domain)
        if zone is None:
            return None, qt, domain
        return zone.get(qt, []), qt, domain if zone else []

    @staticmethod
    def _record_to_bytes(domain_name, record_type, record_ttl, record_value):
        resp = b"\xc0\x0c"
        if record_type == "a":
            resp += b"\x00\x01"
        resp += b"\x00\x01"
        resp += int(record_ttl).to_bytes(4, byteorder="big")
        if record_type == "a":
            resp += b"\x00\x04"
            resp += b"".join([bytes([int(part)]) for part in record_value.split(".")])
        return resp

    def _make_header(self, records_length):
        transaction_id = self._get_transaction_id()
        ancount = records_length.to_bytes(2, byteorder="big")
        if self.format_error:
            self.RCODE = "0001"
        elif not records_length:
            self.RCODE = "0003"
        flags = self._generate_flags()
        return transaction_id + flags + self.QDCOUNT + ancount + self.NSCOUNT + self.ARCOUNT

    def _make_question(self, records_length, record_type, domain_name):
        if self.format_error:
            return b""
        resp = b""
        for part in domain_name:
            length = len(part)
            resp += bytes([length])
            resp += part.encode()
        resp += b"\x00"
        resp += (1).to_bytes(2, byteorder="big")
        resp += (1).to_bytes(2, byteorder="big")
        return resp

    def _make_answer(self, records, record_type, domain_name):
        if not records or self.format_error:
            return b""
        return b"".join([
            self._record_to_bytes(record["name"], record_type, record["ttl"], record["value"])
            for record in records
        ])

    def make_response(self):
        records, record_type, domain_name = self._get_records(self.data[12:])
        if records is None:  # If no records found, query Google DNS
            print(f"No local records found for {domain_name}. Querying Google DNS.")
            return self._forward_to_google(self.data)
        return (
            self._make_header(len(records)) +
            self._make_question(len(records), record_type, domain_name) +
            self._make_answer(records, record_type, domain_name)
        )

    def _forward_to_google(self, request_data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(request_data, (GOOGLE_DNS, GOOGLE_PORT))
        response_data, _ = sock.recvfrom(512)
        return response_data

def start_server():
    """ Start the DNS server """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("0.0.0.0", 53))
    
    print("DNS server started on port 53...")
    
    while True:
        data, addr = server_socket.recvfrom(512)  # DNS packets can be up to 512 bytes
        dns_gen = DNSGen(data)
        response = dns_gen.make_response()
        server_socket.sendto(response, addr)

if __name__ == "__main__":
    start_server()
