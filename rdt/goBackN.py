import random
import time
import threading

class goBackN:
    def __init__(self, senderWindowSize: int) -> None:
        self.senderWindowSize = senderWindowSize
        self.timeout = 4.5
        self.lossProbability = 0.2
        self.forwardChannel = []  # Packets in flight
        self.reverseChannel = []  # ACKs in flight
        self.lastACK = -1  # Last acknowledged packet
        self.base = 0  # First unacknowledged packet
        self.lock = threading.Lock()
        self.stop = False
        self.timers = {}  # Track timers for each packet
    
    def sender(self, packets: int) -> None:
        nextSeqNum = 0  # Next packet to send
        
        def start_timer(seq_num):
            self.timers[seq_num] = time.time()
        
        def check_timeout():
            while not self.stop:
                time.sleep(1)
                with self.lock:
                    if not self.forwardChannel:
                        continue
                    for seq_num in list(self.timers):
                        if time.time() - self.timers[seq_num] > self.timeout:
                            print(f"Sender: Timeout for packet SEQ {seq_num}. Retransmitting...")
                            # Resend all packets from base to nextSeqNum-1
                            for packet in range(self.base, nextSeqNum):
                                print(f"Sender: Retransmitting packet SEQ {packet}.")
                                self.forwardChannel.append(packet)
                                start_timer(packet)

        # Thread to handle timeout
        timeout_thread = threading.Thread(target=check_timeout)
        timeout_thread.start()

        while nextSeqNum < packets:
            while len(self.forwardChannel) >= self.senderWindowSize:
                time.sleep(0.1)

            with self.lock:
                # Send the packet
                self.forwardChannel.append(nextSeqNum)
                start_timer(nextSeqNum)
                print(f"Sender: Sent packet SEQ {nextSeqNum}.")
                nextSeqNum += 1

            time.sleep(random.uniform(1.5, 2.5))  # Simulate varying transmission time
        
        while self.base < packets:
            time.sleep(1)
        
        with self.lock:
            self.stop = True
        timeout_thread.join()  # Wait for timeout thread to finish
    
    def reciever(self) -> None:
        while not self.stop:
            time.sleep(random.uniform(1.5, 2.5))  # Simulate varying processing time
            with self.lock:
                if self.forwardChannel and random.random() > self.lossProbability:  # Simulate packet loss
                    pkt = self.forwardChannel[0]
                    if pkt == self.lastACK + 1:  # In-sequence packet
                        self.lastACK = pkt
                        self.reverseChannel.append(pkt)
                        print(f"Receiver: Received packet SEQ {pkt}. Sending ACK {pkt}.")
                    else:
                        # Duplicate ACK for out-of-order packet
                        self.reverseChannel.append(self.lastACK)
                elif self.forwardChannel:  # Packet lost
                    print(f"Observer: Packet SEQ {self.forwardChannel[0]} lost.")
    
    def backend(self) -> None:
        while not self.stop:
            time.sleep(random.uniform(1.5, 2.5))  # Simulate ACK delay
            with self.lock:
                if self.reverseChannel:
                    ack = self.reverseChannel.pop(0)
                    if ack >= self.base:
                        print(f"Sender: ACK {ack} received.")
                        self.base = ack + 1
                        # Remove acknowledged packets and their timers
                        self.forwardChannel = [pkt for pkt in self.forwardChannel if pkt > ack]
                        self.timers = {seq: timer for seq, timer in self.timers.items() if seq > ack}

    def simulate(self, packets: int) -> None:
        sender_thread = threading.Thread(target=self.sender, args=(packets,))
        receiver_thread = threading.Thread(target=self.reciever)
        backend_thread = threading.Thread(target=self.backend)
        
        sender_thread.start()
        backend_thread.start()
        time.sleep(1)
        receiver_thread.start()
        
        sender_thread.join()
        receiver_thread.join()
        backend_thread.join()

if __name__ == "__main__":
    num_packets = int(input("Enter the number of packets to send: "))
    N = int(input("Enter the sender window size (N): "))
    print("\nSimulating Go Back N Protocol:\n")
    protocol = goBackN(N)
    protocol.simulate(num_packets)
