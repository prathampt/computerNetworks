import random
import time

class Packet:
    def __init__(self, seq_num):
        self.seq_num = seq_num
        self.ack_received = False
        self.timeout = False

class SelectiveRepeat:
    def __init__(self, num_packets, window_size):
        self.num_packets = num_packets
        self.window_size = window_size
        self.packets = [Packet(i) for i in range(num_packets)]
        self.ack_received = [False] * num_packets
        self.timer = [None] * num_packets
        self.send_base = 0
        self.next_seq_num = 0
        self.receiver_buffer = {}
        self.timeout_interval = 5

    def send(self):
        while self.send_base < self.num_packets:
            # Send packets within the window
            while self.next_seq_num < self.send_base + self.window_size and self.next_seq_num < self.num_packets:
                print(f"Sender: Sent packet SEQ {self.next_seq_num}.")
                self.start_timer(self.next_seq_num)
                self.next_seq_num += 1
                time.sleep(random.uniform(1.5, 2.5))

            # Simulate receiving ACKs or packet timeouts
            self.receive_ack()

            # Check for timeout and retransmit packets if needed
            for i in range(self.send_base, min(self.send_base + self.window_size, self.num_packets)):
                if self.timer[i] and time.time() - self.timer[i] > self.timeout_interval:
                    print(f"Sender: Timeout for packet SEQ {i}. Retransmitting.")
                    self.retransmit(i)
                    time.sleep(random.uniform(1.5, 2.5))

            time.sleep(1)  # Simulate time delay

    def receive_ack(self):
        # Simulate random ACK reception
        for i in range(self.send_base, min(self.send_base + self.window_size, self.num_packets)):
            if not self.ack_received[i]:
                # Randomly simulate packet loss or successful delivery
                if random.random() < 0.8:  # 80% chance of successful delivery
                    self.ack_received[i] = True
                    print(f"Receiver: Received packet SEQ {i}.")
                    print(f"Receiver: Delivered packet SEQ {i}. Sending ACK.")
                    time.sleep(random.uniform(1.5, 2.5))
                    print(f"Sender: ACK {i} received.")
                    self.send_base = i + 1  # Move window forward
                else:
                    print(f"Receiver: Packet SEQ {i} lost. No ACK sent.")
    
    def retransmit(self, seq_num):
        # Resend the packet and restart the timer
        print(f"Sender: Retransmitting packet SEQ {seq_num}.")
        self.start_timer(seq_num)

    def start_timer(self, seq_num):
        self.timer[seq_num] = time.time()

if __name__ == "__main__":
    num_packets = int(input("Enter the number of packets to send: "))
    window_size = int(input("Enter the window size: "))
    
    selective_repeat = SelectiveRepeat(num_packets, window_size)
    print("\nSimulating Selective Repeat Protocol:\n")
    selective_repeat.send()
