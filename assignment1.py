"""
IP Calculator: Given the address of the Host or the Network, calculate the various aspects of the subnet...
"""

from typing import List

def calculateIP(address: List[int], netmask: int) -> dict:
    hosts = 2 ** (32 - netmask) - 2
    n = f"Netmask/{netmask}"
    netmaskList = [255] * (netmask // 8)
    netmask %= 8
    netmaskList.append(256 - 2 ** (8 - netmask))
    while len(netmaskList) != 4:
        netmaskList.append(0)
    
    wildcard = [255 ^ num for num in netmaskList]
    
    network = [add & net for add, net in zip(address, netmaskList)]
    broadcast = [add | net for add, net in zip(address, wildcard)]
    hostmin = network.copy()
    hostmin[-1] += 1
    hostmax = broadcast.copy()
    hostmax[-1] -= 1

    return {
        "IP" : {
            "Address" : address, 
            n : netmaskList, 
            "Wildcard" : wildcard,
            "NetworkID" : network,
            "Broadcast" : broadcast,
            "HostMin" : hostmin,
            "HostMax" : hostmax
        }, 
        "Hosts/Net" : hosts
    }

def getBinary(lis: List[int]) -> List[str]:
    binary = []
    for num in lis:
        binary.append(str(bin(num).replace("0b", "")).zfill(8))

    return binary

def formatData(info: dict) -> str:
    data = ""
    for key, value in info["IP"].items():
        data += key + ":\t" + '.'.join(map(lambda x: str(x), value)) + "\t" + '.'.join(getBinary(value)) + '\n'

    data += "Hosts/Net:\t" + str(info["Hosts/Net"])

    return data

def main():
    print("IP Calculator:\n")
    hostIP = input("Enter Host IP Address: ")
    netmask = int(input("Enter netmask (eg. 24): "))
    hostIP = list(map(int, hostIP.split('.')))
    res = calculateIP(hostIP, netmask)
    data = formatData(res)
    print(data)

if __name__=="__main__":
    main()

