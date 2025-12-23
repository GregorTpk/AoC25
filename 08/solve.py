import os, argparse

COMPARE_PAIRS_COUNT_EXAMPLE = 10
COMPARE_PAIRS_COUNT = 1000
COUNTED_CIRCUITS = 3

LOG = False
LOG_LEVEL = 0

def log(s="", log_level=None):
    if LOG and (LOG_LEVEL == -1 or (log_level != None and log_level <= LOG_LEVEL)): print(s)

class JunctionBox:
    """Implementation of union-find: Circuits are defined as a tree of junction boxes. Circuits are
    distinguished by an arbitrary representative which is the tree's root. Each junction box points
    towards the root in order to be able to retrieve the representative."""
    def __init__(self, pos, circuit_representative=None, circuit_size=None):
        self.pos = pos
        if circuit_representative == None:
            #Initially, each circuit consists of just one junction box
            circuit_representative = self
            circuit_size = 1
        self.circuit_representative = circuit_representative
        self.circuit_size = circuit_size
    def __repr__(self):
        return "(%s @ %s) |%s|"%(self.pos, self.get_circuit_representative().pos, self.get_circuit_representative().circuit_size)
    def merge_circuits(self, other_junction_box):
        """Merges the two circuits that self and other_junction_box are part of. Assumes that they are in
        different circuits."""
        my_circ_repr = self.get_circuit_representative()
        other_circ_repr = other_junction_box.get_circuit_representative()

        other_circ_repr.circuit_size += my_circ_repr.circuit_size
        #Attach root of self's circuit to root of other circuit
        my_circ_repr.circuit_representative = other_circ_repr
    def get_circuit_representative(self):
        if self.circuit_representative == self:
            return self
        circuit_representative = self.circuit_representative.get_circuit_representative()
        #Keep it a flat tree
        self.circuit_representative = circuit_representative
        return circuit_representative
    def get_circuit_size(self) -> int:
        return self.get_circuit_representative().circuit_size

class JunctionBoxPair:
    def __init__(self, jbox1, jbox2):
        self.jbox1 = jbox1
        self.jbox2 = jbox2
        self.sq_dist = 0
        for x1, x2 in zip(jbox1.pos, jbox2.pos):
            self.sq_dist += (x1 - x2)**2
    def __repr__(self):
        return "Pair(%s-%s dist=%s)"%(self.jbox1, self.jbox2, self.sq_dist)

def find_largest_circuit_sizes(junction_boxes: list[JunctionBox]) -> list[int]:
    #Collect the COUNTED_CIRCUITS largest circuits sorted by circuit size
    largest_circuits = []
    for jbox in junction_boxes:
        if not jbox.get_circuit_representative() in largest_circuits and (len(largest_circuits) < COUNTED_CIRCUITS or jbox.get_circuit_size() > largest_circuits[-1].get_circuit_size()):
            #Found bigger circuit
            if not largest_circuits or jbox.get_circuit_size() <= largest_circuits[-1].get_circuit_size():
                #Smallest circuit yet and less than COUNTED_CIRCUITS many circuits collected. Just append.
                largest_circuits.append(jbox.get_circuit_representative())
            else:
                #Not smallest circuit to add. Insert to keep order.
                for i, larger_circ in enumerate(largest_circuits):
                    if larger_circ.get_circuit_size() < jbox.get_circuit_size():
                        #Found index to insert at
                        #Insert is slow, though it does not matter since COUNTED_CIRCUITS is small
                        largest_circuits.insert(i, jbox.get_circuit_representative())
                        if len(largest_circuits) > COUNTED_CIRCUITS:
                            #Remove smallest circuit if necessary
                            largest_circuits.pop(-1)
                        break#
    return [circ.get_circuit_size() for circ in largest_circuits]


def solve(filepath: str) -> tuple[int, int]:
    log("Loading...", 0)
    with open(filepath, "r") as f:
        junction_boxes = [JunctionBox([int(pos_comp) for pos_comp in pos.split(",")]) for pos in f.readlines()]

    log(junction_boxes, 2)

    log("Calculate distances...", 0)
    jbox_pairs = []
    for i, jbox1 in enumerate(junction_boxes):
        for jbox2 in junction_boxes[i+1:]:
            jbox_pairs.append(JunctionBoxPair(jbox1, jbox2))

    log("Sort by distance...", 0)
    get_sq_dist = lambda pair: pair.sq_dist
    sorted_jbox_pairs = sorted(jbox_pairs, key=get_sq_dist)

    log(sorted_jbox_pairs, 2)

    log("Connect junction boxes...", 0)
    size_prod = None
    compared_pair_count = 0
    last_connection = None
    for pair in sorted_jbox_pairs:
        compared_pair_count += 1
        #Only merge junction boxes in different circuits
        if pair.jbox1.get_circuit_representative() != pair.jbox2.get_circuit_representative():
            last_connection = pair
            pair.jbox1.merge_circuits(pair.jbox2)
            log("Merge circuits:", 1)
            log(pair.jbox1, 1)
            log(pair.jbox2, 1)
        if compared_pair_count == COMPARE_PAIRS_COUNT:
            log("Calculate product for subproblem a", 0)
            #Subproblem a: Find currently largest circuits
            largest_circ_sizes = find_largest_circuit_sizes(junction_boxes)

            size_prod = 1
            for circ_size in largest_circ_sizes:
                size_prod *= circ_size

    #Subproblem b: Compare junction boxes of last connection
    last_pair_x_prod = last_connection.jbox1.pos[0] * last_connection.jbox2.pos[0]

    return size_prod, last_pair_x_prod

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs="?", default="input.txt", help="Default 'input.txt'")
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help="Only output plain results without text.")
    parser.add_argument('-c', '--compare-pairs-count', type=int, default=COMPARE_PAIRS_COUNT, help="Subproblem a: How many connections before multiplying n largest circuit sizes?")
    parser.add_argument('-e', '--example', action='store_true', default=False, help="Equivalent to --compare-pairs-count=%s to test on example input."%COMPARE_PAIRS_COUNT_EXAMPLE)
    parser.add_argument('-l', '--log', action='store_true', default=False, help="Show log. Tuned by --loglevel")
    parser.add_argument('-L', '--log-level', type=int, default=None, help="The higher the --log-level=0,1,2, the more details. --loglevel=-1 is log all.")
    args = parser.parse_args()

    filepath = args.filepath

    QUIET = args.quiet
    LOG = not QUIET and (args.log or (args.log_level != None))
    if args.log_level == None:
        LOG_LEVEL = 0
    else:
        LOG_LEVEL = args.log_level

    COMPARE_PAIRS_COUNT = args.compare_pairs_count
    if args.example:
        COMPARE_PAIRS_COUNT = COMPARE_PAIRS_COUNT_EXAMPLE


    if os.path.isfile(filepath):
        size_prod, last_pair_x_prod = solve(filepath)
        if QUIET:
            print(size_prod)
            print(last_pair_x_prod)
        else:
            print("a: %s is the product of the sizes of the %s largest circuits after %s connections."%(size_prod, COUNTED_CIRCUITS, COMPARE_PAIRS_COUNT))
            print("b: %s is the product of the X-coordinates of the two junction boxes of the last connection."%(last_pair_x_prod))
    else:
        print("There is no file '%s'"%filepath)
