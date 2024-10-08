

def calculate_and_display_ip_fragmentation(mtu: int, datagram: int, identificationNumber: int) -> None:

    print("Fragment\tDF\tMF\tOffset\tIdentification")
    offsetSize = (mtu - 20) // 8
    offset = 0
    fragmentSize = ((mtu - 20) // 8) * 8
    moreFragment = 1
    datagram -= 20

    while datagram:
        if datagram < fragmentSize:
            moreFragment = 0
            fragmentSize = datagram
        print(f"20 + {fragmentSize}\t0\t{moreFragment}\t{offset}\t{identificationNumber}")
        offset += offsetSize
        datagram -= fragmentSize

    return None

if __name__=="__main__":

    print("IP-Fragmentation Calculator:~")
    print()

    mtu = int(input("Enter Maximum Transfer Unit(MTU): "))
    datagram = int(input("Enter Datagram/Packet Size: "))
    identificationNumber = int(input("Enter the Identification Number: "))
    print()

    calculate_and_display_ip_fragmentation(mtu, datagram, identificationNumber)