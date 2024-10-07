from typing import List
import time

class RouterRIP:
    def __init__(self, name: str, networks: List[str]):
        self.name = name
        self.networks = networks
        # {networkID: (hopCount, nextHop)}
        self.routing_table = {network: (0, None) for network in networks}  # Init table with directly connected networks

    def update_routing_table(self, routerName: str, neighbor_table: dict) -> bool:
        updated = False
        for network, (hopCount, _) in neighbor_table.items():
            newHopCount = hopCount + 1 
            if (network not in self.routing_table) or (newHopCount < self.routing_table[network][0]):
                self.routing_table[network] = (newHopCount, routerName)
                updated = True
        return updated

    def print_routing_table(self):
        print(f"Routing table for Router {self.name}:")
        print("Destination Network\tHop Count\tNext Hop")
        for destination, (cost, next_hop) in self.routing_table.items():
            print(f"{destination}\t\t{cost}\t\t{next_hop}")
        print()


def simulate_rip(routers):
    iteration = 1
    updated = True

    while updated:
        print(f"Iteration {iteration}")
        updated = False
        for router in routers:
            router.print_routing_table()
            time.sleep(2)
            for neighbor in routers:
                if neighbor != router and set(neighbor.networks).intersection(set(router.networks)):
                    if router.update_routing_table(neighbor.name, neighbor.routing_table):
                        updated = True
        iteration += 1
    
    print(f"Iteration {iteration}")

    for router in routers:
        router.print_routing_table()


# Initialize routers with networks they are connected to
router_a = RouterRIP("A", ["192.168.1.0", "10.0.0.0"])
router_b = RouterRIP("B", ["20.0.0.0", "10.0.0.0", "192.168.2.0"])
router_c = RouterRIP("C", ["192.168.3.0", "20.0.0.0"])
# Topology:
# A - B - C

simulate_rip([router_a, router_b, router_c])
