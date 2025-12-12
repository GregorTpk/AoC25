import os, sys

#START_NAME = "you"
START_NAME = "svr"
OUT_NAME = "out"
WAYPOINTS = ["dac", "fft"]

class Node:
    def __init__(self, name, connections):
        self.name = name
        self.connections = connections

        self.explored = False

        if name in WAYPOINTS:
            self.waypoint = 1 << WAYPOINTS.index(name)
        else:
            self.waypoint = 0
        self.waypoint_count = int(name in WAYPOINTS)
        self.num_paths = [0] * (2**len(WAYPOINTS))
    def __repr__(self):
        return "%s(%s)"%(self.name, ",".join((c.name for c in self.connections)))
    def explore(self):
        self.explored = True
        if self.name == OUT_NAME:
            self.num_paths[0] += 1
        for c in self.connections:
            if not c.explored:
                c.explore()
            for i in range(2**len(WAYPOINTS)):
                self.num_paths[i | self.waypoint] += c.num_paths[i]

def solve(filepath):
    nodes = []
    with open(filepath, "r") as f:
        for line in f.readlines():
            node_name, node_connections = line.strip().split(":")
            node_connections = node_connections.strip().split(" ")
            node = Node(node_name, node_connections)
            if node.name == START_NAME:
                startnode = node
            nodes.append(node)

    nodes.append(Node("out", []))

    #Improve: binary search to find connection
    for node in nodes:
        real_connections = []
        for pot_connection in nodes:
            if pot_connection.name in node.connections:
                real_connections.append(pot_connection)
        node.connections = real_connections

    startnode.explore()

    return startnode.num_paths[-1]



if __name__ == "__main__":
    (filepath := sys.argv[1]) if len(sys.argv) >= 2 else (filepath := "input.txt")
    print(solve(filepath)) if os.path.isfile(filepath) else print("There is no such file")
