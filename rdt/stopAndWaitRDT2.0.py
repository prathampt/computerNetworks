import random
import time

class RDT2_0:
    def __init__(self) -> None:
        self.gotNak = False

    def isCorrupted(self) -> bool:
        return random.random() < 0.2
    
    def sendFrame(self, frame: int) -> int:
        print("Sender:", end=" ")
        if self.gotNak: print(f"NAK received. Resending frame {frame}.")
        else: print(f"Sending frame {frame}")
        time.sleep(random.uniform(1.5, 2.5))
        return frame

    def receiveFrame(self, frame: int) -> bool:
        print("Receiver:", end=" ")
        if self.isCorrupted():
            print(f"Received frame {frame}. Frame is corrupted. NAK sent.")
            self.gotNak = True
            time.sleep(random.uniform(1.5, 2.5))
            return False
        else:
            print(f"Received frame {frame}. Frame OK. ACK sent.")
            self.gotNak = False
            time.sleep(random.uniform(1.5, 2.5))
            return True
    
    def simulate(self, num_frames: int) -> None:
        for frame in range(num_frames):
            while not self.receiveFrame(self.sendFrame(frame)):
                pass
        print("All frames sent successfully.")

if __name__ == "__main__":
    num_frames = int(input("Enter the number of frames to send: "))
    print("Simulating RDT 2.0 Protocol:~\n")
    protocol = RDT2_0()
    protocol.simulate(num_frames)