import os, sys, argparse

LOG = False
LOG_LEVEL = 0

def log(s="", log_level=None):
    if LOG and (LOG_LEVEL == -1 or (log_level != None and log_level <= LOG_LEVEL)): print(s)

def binary_search(column, y, a=None, b=None):
    #Returns idx of first vertical edge above or at y if it exists, None otherwise
    #Hints for a, b (also independently) possible

    if a == None:
        a = 0
    if b == None:
        b = len(column) - 1

    while a < b:
        c = (a + b + 1) // 2
        if column[c].edge_coord <= y:
            a = c
        else:
            b = c-1

    if a == b and column[a].edge_coord <= y:
        return a

    return None

class Edge:
    def __init__(self, direction, orientation, edge_coord, edge_step_interv):
        self.direction = int(direction)
        self.orientation = int(orientation)
        self.edge_coord = edge_coord
        self.edge_step_interv = edge_step_interv
    def __repr__(self):
        if not self.direction:
            return "H%s[(%s, %s), (%s, %s)]"%(self.orientation, self.edge_step_interv[0], self.edge_coord, self.edge_step_interv[1], self.edge_coord)
        return "V%s[(%s, %s), (%s, %s)]"%(self.orientation, self.edge_coord, self.edge_step_interv[0], self.edge_coord, self.edge_step_interv[1])

def solve(filepath):
    log("Load", 0)
    with open(filepath, "r") as f:
        width = 0
        height = 0
        tiles = []
        for pos in f.readlines():
            tile = [int(comp) for comp in pos.split(",")]
            tiles.append(tile)
            if tile[0] > width:
                width = tile[0]
            if tile[1] > height:
                height = tile[1]

    log("Setup data structure", 0)

    width += 1
    height += 1

    #Construct edges
    #For each global column: store vertical edges in this column
    all_edges = []
    horizontal_edges = [[] for i in range(width)]
    vertical_edges = [[] for i in range(width)]
    edge_collections = (horizontal_edges, vertical_edges)

    orientation = 0
    for i, tile2 in enumerate(tiles):
        tile1 = tiles[i-1]
        prev_tile = tiles[i-2]
        #Determine direction of edge: horizontal (=0) vertical (=1)
        direction = (tile1[0] == tile2[0])
        edge_collection = edge_collections[direction]

        lower_end, upper_end = sorted((tile1[direction], tile2[direction]))
        edge_coord = tile1[1 - direction]

        flip_orientation = ((prev_tile[not direction] < tile1[not direction]) == (tile1[direction] < tile2[direction]))
        orientation = int(orientation != flip_orientation)

        edge = Edge(direction, orientation, edge_coord, [lower_end, upper_end])
        all_edges.append(edge)

        #Iterate over tiles of edge, foreach: add edge to corresponding list in edge_collection
        for edge_step in range(lower_end, upper_end+1):
            edge_collection[edge_step].append(edge)

    #Sort all vertical-edge collections
    sort_key = lambda edge: edge.edge_coord
    for column in horizontal_edges:
        column.sort(key=sort_key)
    for column in vertical_edges:
        column.sort(key=sort_key)

    #Orient edges correctly
    flip_all_edges = False
    for column in horizontal_edges:
        if column:
            flip_all_edges = not column[0].orientation
            break
    if flip_all_edges:
        for edge in all_edges:
            edge.orientation = 1 - edge.orientation

    log(all_edges, 1)
    log("Horizontal Edges:", 1)
    log(horizontal_edges, 1)
    log("Vertical Edges:", 1)
    log(vertical_edges, 1)
    log("", 1)

    def check_rectangle(p1, p2):
        log("", 2)
        log("Checking rectangle %s-%s"%(p1, p2), 2)

        low_x, high_x = sorted((p1[0], p2[0]))
        low_y, high_y = sorted((p1[1], p2[1]))
        #sorted_corners = (((low_x, low_y), (low_x, high_y)), ((high_x, low_y), (high_x, high_y)))

        #Access [edge_direction][rectangle_side]
        sorted_edge_coords = ((low_y, high_y), (low_x, high_x))

        #Check both directions of the rectangle's edges separately (horizontal, vertical)
        for edge_dir in (0, 1):
            log("edge_dir = %s"%edge_dir, 3)
            perp_edge_coll = edge_collections[1 - edge_dir]

            is_slim_rectangle = (sorted_edge_coords[edge_dir][0] == sorted_edge_coords[edge_dir][1])
            log("slim = %s"%is_slim_rectangle, 3)

            #Both sides (low i.e. left/top, high i.e. right/bottom)
            for rectangle_side in (0, 1):
                log("rectangle_side = %s"%rectangle_side, 3)
                edge_coord = sorted_edge_coords[edge_dir][rectangle_side]
                log("edge_coord = %s"%edge_coord, 3)
                low_perp_edge_coord, high_perp_edge_coord = sorted_edge_coords[1 - edge_dir]

                high_perp_edge_idx = binary_search(perp_edge_coll[edge_coord], high_perp_edge_coord)
                low_perp_edge_idx = binary_search(perp_edge_coll[edge_coord], low_perp_edge_coord, b=high_perp_edge_idx)

                if low_perp_edge_idx == None or high_perp_edge_idx == None:
                    return False

                #Start at lower corner. Check until high corner. Steps given by coords of perpendicular edges
                low_edge_step, high_edge_step = sorted_edge_coords[1 - edge_dir]
                edge_step = low_edge_step

                while edge_step <= high_edge_step:
                    log("edge_step = %s"%edge_step, 4)
                    log("perp idxs = (%s, %s)"%(low_perp_edge_idx, high_perp_edge_idx), 4)
                    #Possibility 1: inside proven by perpendicular edge
                    #1.1: edge_step lies on perpendicular edge
                    if perp_edge_coll[edge_coord][low_perp_edge_idx].edge_coord == edge_step:
                        log("1.1", 4)
                        edge_step += 1
                        low_perp_edge_idx = binary_search(perp_edge_coll[edge_coord], edge_step, a=low_perp_edge_idx, b=high_perp_edge_idx)
                        continue
                    #1.2 edge_step lies on inner side of next perpendicular edge
                    elif perp_edge_coll[edge_coord][low_perp_edge_idx].orientation:
                        log("1.2", 4)
                        low_perp_edge_idx += 1
                        if low_perp_edge_idx <= len(perp_edge_coll[edge_coord]) - 1:
                            edge_step = perp_edge_coll[edge_coord][low_perp_edge_idx].edge_coord + 1
                        else:
                            edge_step = high_edge_step + 1
                        continue

                    #Possibility 2: inside proven by parallel edge
                    parallel_edge_idx = binary_search(edge_collections[edge_dir][edge_step], edge_coord)
                    if parallel_edge_idx == None:
                        return False
                    parallel_edge = edge_collections[edge_dir][edge_step][parallel_edge_idx]
                    if parallel_edge.edge_coord == edge_coord:
                        edge_step = parallel_edge.edge_step_interv[1] + 1
                        #2.1: Good case: Slim rectangle or edge oriented towards inside of rectangle
                        if is_slim_rectangle or parallel_edge.orientation != rectangle_side:
                            log("2.1", 4)
                            low_perp_edge_idx = binary_search(perp_edge_coll[edge_coord], edge_step, a=low_perp_edge_idx, b=high_perp_edge_idx)
                            continue
                        #2.2: Bad case: Edge oriented towards outside of rectangle: Recursive divide and conquer
                        log("BAD case", 3)
                        #Check if remaining current edge is inside
                        if edge_step <= high_edge_step:
                            if not edge_dir:
                                q1 = [edge_step, edge_coord]
                                q2 = [high_edge_step, edge_coord]
                            else:
                                q1 = [edge_coord, edge_step]
                                q2 = [edge_coord, high_edge_step]
                            if not check_rectangle(q1, q2):
                                return False
                        #Check if rectangle minus current edge is inside
                        delta = (1 if rectangle_side == 0 else -1)
                        if not edge_dir:
                            q1 = [low_edge_step, edge_coord + delta]
                            q2 = [high_edge_step, edge_coord + delta]
                        else:
                            q1 = [edge_coord + delta, low_edge_step]
                            q2 = [edge_coord + delta, high_edge_step]
                        return check_rectangle(q1, q2)

                    #No case occured, not inside
                    return False
        return True

    max_area = 0

    log("Iterate pairs", 0)
    for i, p1 in enumerate(tiles):
        for p2 in tiles[i+1:]:
            area = ((abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1))
            if area > max_area and check_rectangle(p1, p2):
                log("New max area = %s"%area, 1)
                max_area = area

    return max_area

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs="?", default="input.txt", help="Default 'input.txt'")
    parser.add_argument('-l', '--log', action='store_true', default=False, help="Show log. Tuned by --loglevel")
    parser.add_argument('-L', '--loglevel', type=int, default=-1, help="The higher the --loglevel=0,...,4, the more details. --loglevel=-1 is log all.")
    args = parser.parse_args()

    filepath = args.filepath
    LOG_LEVEL = args.loglevel
    LOG = args.log or (LOG_LEVEL != -1)

    print(solve(filepath)) if os.path.isfile(filepath) else print("There is no such file")
