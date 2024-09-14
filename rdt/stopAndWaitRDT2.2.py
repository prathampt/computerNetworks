import random
import time

class RDT2_2:
    def __init__(self) -> None:
        self.SEQ = 0
        self.expectedACK = -1
        self.ackSent = -1
        self.nextFrame = False

    def isCorrupted(self) -> bool:
        return random.random() < 0.2
    
    def isResponseCorrupted(self) -> bool:
        return random.random() > 0.8
    
    def sendFrame(self, frame: int) -> int:
        if self.isResponseCorrupted():
            print(f"Sender: Response corrupted. Resending frame {frame} [SEQ {frame % 2}].")
        elif self.expectedACK != self.ackSent:
            print(f"Sender: Previous ACK {1 - self.SEQ} received. Resending frame {frame} [SEQ {frame % 2}].") 
        else: 
            self.nextFrame = True
        time.sleep(random.uniform(1.5, 2.5))
        

    def justSend(self, frame: int) -> int:
        print(f"Sender: Sending frame {frame} [SEQ {frame % 2}].")
        self.nextFrame = False
        self.expectedACK = frame % 2
        time.sleep(random.uniform(1.5, 2.5))
        return frame

    def receiveFrame(self, frame: int) -> bool:
        print("Receiver:", end=" ")
        if self.isCorrupted():
            print(f"Received frame {frame} [SEQ {frame % 2}]. Frame is corrupted. Previous ACK {1 - self.SEQ} sent.")
            self.ackSent = 1 - self.SEQ
            time.sleep(random.uniform(1.5, 2.5))
            return False
        else:
            if self.SEQ != frame % 2:
                print(f"Received frame {frame} [SEQ {frame % 2}] dropped. Frame is out of order. Previous ACK {1 - self.SEQ} sent.")
                time.sleep(random.uniform(1.5, 2.5))
                self.ackSent = 1 - self.SEQ
                return True
            print(f"Received frame {frame} [SEQ {frame % 2}]. Frame OK. ACK {self.SEQ} sent.")
            self.ackSent = self.SEQ
            self.SEQ = 1 - self.SEQ
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
    print("Simulating RDT 2.2 Protocol:~\n")
    protocol = RDT2_2()
    protocol.simulate(num_frames)