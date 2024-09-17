import random
import matplotlib.pyplot as plt

# Simulation Parameters
MAX_ROUNDS = 50
LOSS_PROBABILITY = 0.1  # Probability of packet loss
initial_ssthresh = 32   # Initial threshold
initial_cwnd = 1        # Initial congestion window

class TCP:
    def __init__(self, ssthresh, cwnd, name="TCP"):
        self.ssthresh = ssthresh
        self.cwnd = cwnd
        self.name = name
        self.history = []
    
    def simulate_round(self, round_num):
        """Simulate one round of sending packets."""
        self.history.append(self.cwnd)
        print(f"{self.name} Round {round_num}: cwnd={self.cwnd}, ssthresh={self.ssthresh}")
        
        # Simulate packet loss
        if random.random() < LOSS_PROBABILITY:
            return False  # Packet loss occurred
        return True  # No packet loss
    
    def plot(self):
        """Plot the history of congestion window changes."""
        plt.plot(self.history, label=self.name)
        plt.xlabel('Round Number')
        plt.ylabel('Congestion Window (cwnd)')
        plt.title(f'{self.name} Congestion Control')
        plt.legend()
        plt.show()


class TCPSlowStart(TCP):
    def simulate(self):
        for round_num in range(MAX_ROUNDS):
            if not self.simulate_round(round_num):  # Packet loss
                self.ssthresh = max(self.cwnd // 2, 1)
                self.cwnd = 1
                print(f"Packet loss! New ssthresh={self.ssthresh}, cwnd={self.cwnd}")
            else:
                if self.cwnd < self.ssthresh:
                    self.cwnd *= 2  # Exponential growth
                else:
                    self.cwnd += 1  # Linear growth


class TCPAIMD(TCP):
    def simulate(self):
        for round_num in range(MAX_ROUNDS):
            if not self.simulate_round(round_num):  # Packet loss
                self.ssthresh = max(self.cwnd // 2, 1)
                self.cwnd = max(1, self.cwnd // 2)
                print(f"Packet loss! New ssthresh={self.ssthresh}, cwnd={self.cwnd}")
            else:
                if self.cwnd < self.ssthresh:
                    self.cwnd *= 2  # Slow start phase (exponential growth)
                else:
                    self.cwnd += 1  # AIMD phase (linear growth)


class TCPTahoe(TCPAIMD):
    def simulate(self):
        for round_num in range(MAX_ROUNDS):
            if not self.simulate_round(round_num):  # Packet loss
                self.ssthresh = max(self.cwnd // 2, 1)
                self.cwnd = 1  # Reset cwnd to 1 (Tahoe behavior)
                print(f"Packet loss! New ssthresh={self.ssthresh}, cwnd={self.cwnd}")
            else:
                if self.cwnd < self.ssthresh:
                    self.cwnd *= 2  # Exponential growth
                else:
                    self.cwnd += 1  # Linear growth


class TCPReno(TCPAIMD):
    def simulate(self):
        fast_recovery = False
        for round_num in range(MAX_ROUNDS):
            if fast_recovery:
                # Fast Recovery: continue linear growth after loss
                self.cwnd += 1
                fast_recovery = False
            elif not self.simulate_round(round_num):  # Packet loss
                self.ssthresh = max(self.cwnd // 2, 1)
                self.cwnd = self.ssthresh  # Fast recovery, cwnd reduced to half
                fast_recovery = True
                print(f"Packet loss! New ssthresh={self.ssthresh}, cwnd={self.cwnd}")
            else:
                if self.cwnd < self.ssthresh:
                    self.cwnd *= 2  # Exponential growth
                else:
                    self.cwnd += 1  # Linear growth


# Run simulations
def run_simulation():
    tcp_slow_start = TCPSlowStart(initial_ssthresh, initial_cwnd, "TCP Slow Start")
    tcp_slow_start.simulate()
    tcp_slow_start.plot()

    tcp_aimd = TCPAIMD(initial_ssthresh, initial_cwnd, "TCP AIMD")
    tcp_aimd.simulate()
    tcp_aimd.plot()

    tcp_tahoe = TCPTahoe(initial_ssthresh, initial_cwnd, "TCP Tahoe")
    tcp_tahoe.simulate()
    tcp_tahoe.plot()

    tcp_reno = TCPReno(initial_ssthresh, initial_cwnd, "TCP Reno")
    tcp_reno.simulate()
    tcp_reno.plot()

run_simulation()
