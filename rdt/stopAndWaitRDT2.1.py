import random
import time

class RDT2_1:
    def __init__(self) -> None:
        self.SEQ = 0
        self.gotNak = False
        self.nextFrame = False

    def isCorrupted(self) -> bool:
        return random.random() < 0.2
    
    def isResponseCorrupted(self) -> bool:
        return random.random() > 0.8
    
    def sendFrame(self, frame: int) -> int:
        responseCorrupted = self.isResponseCorrupted()
        if self.gotNak or responseCorrupted: 
            print("Sender:", end=" ")
            if responseCorrupted:
                print(f"Response corrupted. Resending frame {frame}.")
            else:
                print(f"NAK received. Resending frame {frame}.") 
        else: 
            self.nextFrame = True
        time.sleep(random.uniform(1.5, 2.5))
        

    def justSend(self, frame: int) -> int:
        print(f"Sender: Sending frame {frame}.")
        self.nextFrame = False
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
            if self.SEQ != frame % 2:
                print(f"Received frame {frame} dropped. Frame is out of order. ACK sent.")
                time.sleep(random.uniform(1.5, 2.5))
                self.gotNak = False
                return True
            print(f"Received frame {frame}. Frame OK. ACK sent.")
            self.SEQ = 1 - self.SEQ
            self.gotNak = False
            time.sleep(random.uniform(1.5, 2.5))
            return True
    
    def simulate(self, num_frames: int) -> None:
        for frame in range(num_frames):
            self.justSend(frame)
            while not self.nextFrame:
                self.receiveFrame(frame)
                self.sendFrame(frame)
        print("All frames sent successfully.")

if __name__ == "__main__":
    num_frames = int(input("Enter the number of frames to send: "))
    print("Simulating RDT 2.1 Protocol:~\n")
    protocol = RDT2_1()
    protocol.simulate(num_frames)