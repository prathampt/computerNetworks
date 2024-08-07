"""
IP Calculator: Given the address of the Host or the Network, calculate the various aspects of the subnet...
"""
import tkinter as tk
from tkinter import ttk
from typing import List

def calculateIP(address: List[int], netmask: int) -> dict:
    cls = ""
    noOfSubnets = 0
    if address[0] == 127:
        cls = "Loop Back"
    elif address[0] & 128 == 0:
        cls = "Class A"
        noOfSubnets = 2 ** (netmask - 8)
    elif address[0] & 64 == 0:
        cls = "Class B"
        noOfSubnets = 2 ** (netmask - 16)
    elif address[0] & 32 == 0:
        cls = "Class C"
        noOfSubnets = 2 ** (netmask - 24)
    else:
        cls = "Class D (Research)"
    hosts = 2 ** (32 - netmask) - 2
    netmaskStr = f"Netmask/{netmask}"
    netmaskList = [255] * (netmask // 8)
    netmask %= 8
    if netmask:
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
            netmaskStr : netmaskList, 
            "Wildcard" : wildcard,
            "NetworkID" : network,
            "Broadcast" : broadcast,
            "HostMin" : hostmin,
            "HostMax" : hostmax
        }, 
        "Number of Subnets" : noOfSubnets,
        "Number of IP's per Subnet" : hosts, 
        "Class" : cls
    }

def getBinary(lis: List[int]) -> List[str]:
    return [format(num, '08b') for num in lis]

def formatData(info: dict) -> str:
    data = ""
    for key, value in info["IP"].items():
        data += key + ":\t" + '.'.join(map(lambda x: str(x), value)) + "\t" + '.'.join(getBinary(value)) + '\n'

    data += "Number of Subnets:\t" + str(info["Number of Subnets"]) + "\n"
    data += "Number of IP's per Subnet:\t" + str(info["Number of IP's per Subnet"]) + "\n"
    data += "Class:\t" + str(info["Class"])

    return data

def mainCLI():
    print("IP Calculator:\n")
    hostIP = input("Enter Host IP Address: ")
    netmask = int(input("Enter netmask (eg. 24): "))
    if netmask in [31, 32]: 
        print("Sorry! /32 and /31 SubNet is not possible...")
        return None
    hostIP = list(map(int, hostIP.split('.')))
    res = calculateIP(hostIP, netmask)
    data = formatData(res)
    print(data)

def mainGUI():

    def calculate_and_display():
        host_ip = entry_ip.get()
        netmask = int(entry_netmask.get())
        if netmask in [31, 32]: 
            tree.insert('', 'end', values=("Sorry!!!", "/31 and /32 SubNet isn't possible..."))
            return None
        host_ip = list(map(int, host_ip.split('.')))
        res = calculateIP(host_ip, netmask)
        formatted_data = formatDataForTable(res)
        
        # Clear the treeview
        for item in tree.get_children():
            tree.delete(item)
        
        # Insert new data
        for key, value in formatted_data.items():
            tree.insert('', 'end', values=(key, value[0], value[1]))

    def formatDataForTable(info: dict) -> dict:
        formatted_data = {}
        for key, value in info["IP"].items():
            formatted_data[key] = ('.'.join(map(str, value)), '.'.join(getBinary(value)))
        formatted_data["Number of Subnets"] = (str(info["Number of Subnets"]), "")
        formatted_data["Number of IP's per Subnet"] = (str(info["Number of IP's per Subnet"]), "")
        formatted_data["Class"] = (str(info["Class"]), "")
        return formatted_data

    # Create the main window
    root = tk.Tk()
    root.title("IP Calculator")
    root.geometry("700x500")
    root.configure(bg="#2c3e50")

    # Create and place the input fields
    frame = ttk.Frame(root, padding="10", style="TFrame")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

    style = ttk.Style()
    style.configure("TLabel", foreground="#ecf0f1", background="#2c3e50", font=("Helvetica", 12))
    style.configure("TButton", foreground="#2c3e50", background="#ecf0f1", font=("Helvetica", 12, "bold"))
    style.configure("TFrame", background="#2c3e50")
    style.configure("TEntry", font=("Helvetica", 12))

    ttk.Label(frame, text="Enter Host IP Address:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    entry_ip = ttk.Entry(frame, width=20, font=("Helvetica", 12))
    entry_ip.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    ttk.Label(frame, text="Enter netmask (e.g., 24):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    entry_netmask = ttk.Entry(frame, width=10, font=("Helvetica", 12))
    entry_netmask.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    # Create and place the calculate button
    calculate_button = ttk.Button(frame, text="Calculate", command=calculate_and_display, style="TButton")
    calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Create and place the output table
    output_frame = ttk.Frame(root, padding="10", style="TFrame")
    output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

    columns = ('Property', 'Decimal', 'Binary')
    tree = ttk.Treeview(output_frame, columns=columns, show='headings', height=15)
    tree.heading('Property', text='Property')
    tree.heading('Decimal', text='Decimal')
    tree.heading('Binary', text='Binary')

    tree.column('Property', anchor=tk.W, width=200)
    tree.column('Decimal', anchor=tk.W, width=200)
    tree.column('Binary', anchor=tk.W, width=300)

    tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    scroll = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scroll.set)
    scroll.grid(row=0, column=1, sticky='ns')

    # Run the application
    root.mainloop()

if __name__=="__main__":
    # mainCLI()
    mainGUI()
