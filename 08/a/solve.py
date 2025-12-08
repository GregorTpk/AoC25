import os, sys

#CONNECT_COUNT = 1000
#COUNTED_CIRCUITS = 3
CONNECT_COUNT = 1000
COUNTED_CIRCUITS = 3

class CircuitPart:
    def __init__(self, pos, representative=None, size=None):
        self.pos = pos
        if representative == None:
            representative = self
            size = 1
        self.representative = representative
        self.size = size
    def __repr__(self):
        return "(%s @ %s) |%s|"%(self.pos, self.get_repr().pos, self.get_repr().size)
    def merge(self, circ_part):
        my_repr = self.get_repr()
        other_repr = circ_part.get_repr()

        other_repr.size += my_repr.size
        my_repr.representative = other_repr
    def get_repr(self):
        if self.representative == self:
            return self.representative
        representative = self.representative.get_repr()
        self.representative = representative
        return representative
    def get_size(self):
        return self.get_repr().size

class Pair:
    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2
        self.sq_dist = 0
        for x1, x2 in zip(part1.pos, part2.pos):
            self.sq_dist += (x1 - x2)**2
    def __repr__(self):
        return "%s-%s |%s|"%(self.part1, self.part2, self.sq_dist)

def solve(filepath):
    with open(filepath, "r") as f:
        circuits = [CircuitPart([int(comp) for comp in pos.split(",")]) for pos in f.readlines()]

    print(circuits)

    distances = []
    for i, part1 in enumerate(circuits):
        for part2 in circuits[i+1:]:
            distances.append(Pair(part1, part2))

    print("sorting...")
    key_func = lambda pair: pair.sq_dist
    sorted_distances = sorted(distances, key=key_func)
    print("sorted!")

    print(sorted_distances)

    i = 0
    last_connection = None
    for pair in sorted_distances:
        i += 1
        if pair.part1.get_repr() != pair.part2.get_repr():
            last_connection = pair
            pair.part1.merge(pair.part2)
            print("Merge:")
            print(pair.part1)
            print(pair.part2)
#        if i == CONNECT_COUNT:
#            break

    print()

    largest_circuits = []
    for part in circuits:
        print(part)
        if not part.get_repr() in largest_circuits and (len(largest_circuits) < COUNTED_CIRCUITS or part.get_size() > largest_circuits[-1].get_size()):
            print("insert")
            #Found bigger circuit
            if not largest_circuits or part.get_size() <= largest_circuits[-1].get_size():
                largest_circuits.append(part.get_repr())
            else:
                for i, circ in enumerate(largest_circuits):
                    if circ.get_size() < part.get_size():
                        largest_circuits.insert(i, part.get_repr())
                        if len(largest_circuits) > COUNTED_CIRCUITS:
                            largest_circuits.pop(-1)
                        break

            print(largest_circuits)

    size_prod = 1
    for c in largest_circuits:
        print("Circuit with size %s"%c.get_size())
        size_prod *= c.get_size()

    last_pair_x_prod = last_connection.part1.pos[0] * last_connection.part2.pos[0]

    return last_pair_x_prod
    #return size_prod

if __name__ == "__main__":
    (filepath := sys.argv[1]) if len(sys.argv) >= 2 else (filepath := "input.txt")
    print(solve(filepath)) if os.path.isfile(filepath) else print("There is no such file")
