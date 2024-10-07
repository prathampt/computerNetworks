from typing import List, Dict, Tuple
import heapq
import time

class RouterOSPF:
    def __init__(self, name: str, networks: List[str], link_costs: Dict[str, int]):
        self.name = name
        self.networks = networks  # List of networks the router is directly connected to
        self.link_costs = link_costs  # {neighborName: cost}
        self.lsdb = {}  # Link-State Database (other routers' LSAs)
        # Routing table {networkID: (cost, nextHop)}
        self.routing_table = {network: (0, None) for network in networks}  # Init table with directly connected networks

    def flood_lsa(self, routers: List['RouterOSPF']):
        """Flood the LSA (Link-State Advertisement) to all other routers."""
        for router in routers:
            if router != self:
                router.receive_lsa(self.name, self.networks, self.link_costs)

    def receive_lsa(self, router_name: str, networks: List[str], link_costs: Dict[str, int]):
        """Receive an LSA from a neighboring router and store it in the LSDB."""
        self.lsdb[router_name] = (networks, link_costs)

    def compute_routing_table(self):
        """Run Dijkstra's algorithm to compute the shortest path to all routers and networks."""
        # Initialize distances and previous hops
        dist = {self.name: 0}  # Distance from this router to every other router (start with itself)
        prev = {self.name: None}  # Previous router on the shortest path (to find next hops)
        pq = [(0, self.name)]  # Priority queue for Dijkstra's algorithm: (cost, routerName)

        # Dijkstra's algorithm: explore all routers
        while pq:
            current_cost, current_router = heapq.heappop(pq)

            # Explore all neighbors of the current router (including itself)
            if current_router == self.name:
                neighbors = self.link_costs
            else:
                neighbors = self.lsdb.get(current_router, ([], {}))[1]

            for neighbor, cost in neighbors.items():
                new_cost = current_cost + cost
                if new_cost < dist.get(neighbor, float('inf')):
                    dist[neighbor] = new_cost
                    prev[neighbor] = current_router
                    heapq.heappush(pq, (new_cost, neighbor))

        # Update routing table with networks from all routers
        for router_name, router_dist in dist.items():
            if router_name == self.name:
                continue

            # Trace back to find the correct next hop
            next_hop = router_name
            while prev[next_hop] != self.name:
                next_hop = prev[next_hop]

            # Update routing table with the networks of the current router
            networks, _ = self.lsdb.get(router_name, ([], {}))
            for network in networks:
                if network not in self.routing_table or router_dist < self.routing_table[network][0]:
                    self.routing_table[network] = (router_dist, next_hop)

    def print_routing_table(self):
        """Print the router's current routing table."""
        print(f"Routing table for Router {self.name}:")
        print("Destination Network\tCost\tNext Hop")
        for destination, (cost, next_hop) in self.routing_table.items():
            print(f"{destination}\t\t{cost}\t\t{next_hop}")
        print()

def simulate_ospf(routers: List[RouterOSPF]):
    """Simulate the OSPF protocol by flooding LSAs and computing routing tables."""
    iteration = 1
    print(f"Iteration {iteration}: Flood LSAs")
    
    # Flood LSAs to initialize the LSDB in all routers
    for router in routers:
        router.flood_lsa(routers)
    
    time.sleep(1)  # Simulate delay in flooding LSAs
    
    # Compute routing tables after LSAs are flooded
    for router in routers:
        router.compute_routing_table()

    iteration += 1
    print(f"Iteration {iteration}: Print routing tables")
    
    # Print the final routing tables
    for router in routers:
        router.print_routing_table()

# Initialize routers by specifying networks they are connected to and link costs to neighbors
router_a = RouterOSPF("A", ["192.168.1.0", "10.0.0.0"], {"B": 1})
router_b = RouterOSPF("B", ["20.0.0.0", "10.0.0.0", "192.168.2.0"], {"A": 1, "C": 2})
router_c = RouterOSPF("C", ["192.168.3.0", "20.0.0.0"], {"B": 2})

# Topology:
# A --1-- B --2-- C

routers_by_name = {
    "A": router_a,
    "B": router_b,
    "C": router_c
}

simulate_ospf([router_a, router_b, router_c])
