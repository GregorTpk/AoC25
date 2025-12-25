import os, argparse

"""
Algorithm is a recursive implementation of a modified DFS.

A Node-object has the attribute node.num_paths, which is a list that stores all numbers of distinct paths from node to 'out'. More specifically, for bits b_0, ..., b_n the number of paths which
visit exactly the waypoints w_i s.t. b_i == 1 is stored in node.num_paths[idx] with index

idx = b_n * 2**n + ... + b_0 * 2**0.
"""

#A subproblem consists of (startnode, [waypoints])
SUBPROBLEMS = (["you", []],
               ["svr", ["dac", "fft"]])

OUT_NAME = "out"

class Node:
    def __init__(self, name, connections):
        self.name = name
        self.connections = connections

        # Attributes that are changed during DFS
        self.waypoint_count = None
        self.waypoint = None
        self.explored = None
        self.num_paths = None
    def __repr__(self):
        return "%s(%s)"%(self.name, ",".join((c.name for c in self.connections)))
    @staticmethod
    def reset_graph(nodes, waypoints):
        for node in nodes:
            node.reset(waypoints)
    def reset(self, waypoints):
        "Reset self for another DFS"
        self.waypoint_count = len(waypoints)
        if self.name in waypoints:
            self.waypoint = 1 << waypoints.index(self.name)
        else:
            self.waypoint = 0
        self.explored = False
        self.num_paths = [0] * (2**len(waypoints))
    def explore(self):
        """Modified recursive DFS"""
        self.explored = True
        if self.name == OUT_NAME:
            self.num_paths[0] += 1
        for c in self.connections:
            if not c.explored:
                #Recursive search
                c.explore()
            for i in range(2**self.waypoint_count):
                #Extend all paths from a neighbor c to 'out' by self
                #If necessary, take into account self being a waypoint when storing the path count
                self.num_paths[i | self.waypoint] += c.num_paths[i]

def load_graph(filepath: str) -> list[Node]:
    """Loads file and builds graph as a list of Node-objects."""

    #Build list of all nodes
    nodes = []
    with open(filepath, "r") as f:
        for line in f.readlines():
            node_name, node_connections = line.strip().split(":")
            node_connections = node_connections.strip().split(" ")
            node = Node(node_name, node_connections)
            nodes.append(node)

    nodes.append(Node(OUT_NAME, []))

    #Make connections between nodes
    #Improve: binary search to find connection
    for node in nodes:
        real_connections = []
        for pot_connection in nodes:
            if pot_connection.name in node.connections:
                real_connections.append(pot_connection)
        node.connections = real_connections

    return nodes

def solve(filepath: str) -> list[int]:
    nodes = load_graph(filepath)
    get_startnode = lambda startname: next((node for node in nodes if node.name == startname), None)

    results = []

    for startname, waypoints in SUBPROBLEMS:
        startnode = get_startnode(startname)
        Node.reset_graph(nodes, waypoints)

        startnode.explore()
        results.append(startnode.num_paths[-1])

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs="?", default="input.txt", help="Default 'input.txt'")
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help="Only output plain results without text.")
    args = parser.parse_args()

    filepath = args.filepath

    QUIET = args.quiet

    if os.path.isfile(filepath):
        solutions = solve(filepath)
        if not QUIET:
            for sol, problem in zip(solutions, SUBPROBLEMS):
                print("There are %s distinct paths from '%s' via waypoints %s to '%s'."%(sol, problem[0], problem[1], OUT_NAME))
        else:
            for sol in solutions:
                print(sol)
    else:
        print("There is no such file")

