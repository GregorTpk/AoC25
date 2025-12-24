import os, argparse

LOG = False
LOG_LEVEL = 0

"""
Data structure:
Edge is a container-class for storing data of an edge between two neighboring red tiles.

Foreach x- and y-position, i.e. for each column and each row:
horizontal_edges[x] is a sorted list containing all horizontal edges which intersect the column at x.
It is sorted by y-position of the horizontal edges.
Similarly, vertical_edges[y] is a sorted list containing all vertical edges which intersect the column at y.
It is sorted by x-position of the vertical edges.

"""

def log(s="", log_level=None):
    if LOG and (LOG_LEVEL == -1 or (log_level != None and log_level <= LOG_LEVEL)): print(s)

def binary_search(edge_collection, edge_coord, lower_bound=None, upper_bound=None):
    """Returns idx of first edge with edge coordinate lower than or equal to edge_coord if it exists, None otherwise.
    Hints for lower_bound, upper_bound (also only lower_bound/only upper_bound) possible."""

    if lower_bound == None:
        lower_bound = 0
    if upper_bound == None:
        upper_bound = len(edge_collection) - 1

    while lower_bound < upper_bound:
        mid = (lower_bound + upper_bound + 1) // 2
        if edge_collection[mid].edge_coord <= edge_coord:
            lower_bound = mid
        else:
            upper_bound = mid-1

    if lower_bound == upper_bound and edge_collection[lower_bound].edge_coord <= edge_coord:
        return lower_bound

    return None

class Edge:
    """Container class for an edge between two neighboring red tiles.
    direction: horizontal (=0) or vertical (=1) edge.
    orientation: inner side lies above/left (=0) or below/right (=1) of edge depending on its direction.
    edge_coord: y- or x-pos of a horizontal or vertical edge respectively.
    edge_step_interv: [min x-pos, max x-pos] or [min y-pos, max y-pos] respectively of the tiles of the horizontal or vertical edge."""
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
    #List of all red tiles
    tiles = []
    with open(filepath, "r") as f:
        width = 0
        height = 0
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

    #Construct collections of horizontal and vertical edges
    all_edges = []
    horizontal_edges = [[] for col in range(width)]
    vertical_edges = [[] for row in range(height)]
    edge_collections = (horizontal_edges, vertical_edges)

    #Start with an arbitrary edge orientation and flip all orientations afterwards if necessary
    orientation = 0

    for i, tile2 in enumerate(tiles):
        #tile1, tile2 are two neighboring red tiles defining an edge
        tile1 = tiles[i-1]

        #Determine direction of edge: horizontal (=0) vertical (=1)
        direction = (tile1[0] == tile2[0])
        edge_collection = edge_collections[direction]

        #Get edge coord and edge steps which depend on the orientation
        edge_coord = tile1[1 - direction]
        lower_end, upper_end = sorted((tile1[direction], tile2[direction]))

        #Determining edge orientation requires previous edge:
        #Right turn from horizontal to vertical edge and left turn from vertical to horizontal edge both flip the orientation.
        #Otherwise the orientations are the same
        prev_tile = tiles[i-2]
        flip_orientation = ((prev_tile[not direction] < tile1[not direction]) == (tile1[direction] < tile2[direction]))
        orientation = int(orientation != flip_orientation)

        edge = Edge(direction, orientation, edge_coord, [lower_end, upper_end])
        all_edges.append(edge)

        #Iterate over tiles of edge, foreach: add edge to corresponding list in edge_collection
        for edge_step in range(lower_end, upper_end+1):
            edge_collection[edge_step].append(edge)

    #Sort both edge collections by edge_coord
    log("Sort edge collections", 0)
    sort_key = lambda edge: edge.edge_coord
    for column in horizontal_edges:
        column.sort(key=sort_key)
    for column in vertical_edges:
        column.sort(key=sort_key)

    #Orient edges correctly by flipping if necessary
    log("Flip orientations if necessary", 0)
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

    def check_rectangle(p1: list[int, int], p2: list[int, int]) -> bool:
        """Checks whether the rectangle spanned by p1, p2 is inside, i.e. consists of red and green tiles only.
        Does not require p1 and p2 to be red tiles."""
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
                low_perp_edge_idx = binary_search(perp_edge_coll[edge_coord], low_perp_edge_coord, upper_bound=high_perp_edge_idx)

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
                        low_perp_edge_idx = binary_search(perp_edge_coll[edge_coord], edge_step, lower_bound=low_perp_edge_idx, upper_bound=high_perp_edge_idx)
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
                            low_perp_edge_idx = binary_search(perp_edge_coll[edge_coord], edge_step, lower_bound=low_perp_edge_idx, upper_bound=high_perp_edge_idx)
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

    max_arbitrary_rect = 0 # For subproblem a
    max_strict_rect = 0 # For subproblem b

    log("Iterate pairs", 0)
    for i, p1 in enumerate(tiles):
        for p2 in tiles[i+1:]:
            area = ((abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1))

            if area > max_arbitrary_rect:
                max_arbitrary_rect = area

            if area > max_strict_rect and check_rectangle(p1, p2):
                log("New max area = %s"%area, 1)
                max_strict_rect = area

    return max_arbitrary_rect, max_strict_rect

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs="?", default="input.txt", help="Default 'input.txt'")
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help="Only output plain results without text.")
    parser.add_argument('-l', '--log', action='store_true', default=False, help="Show log. Tuned by --loglevel")
    parser.add_argument('-L', '--log-level', type=int, default=None, help="The higher the --log-level=0,...,4, the more details. --loglevel=-1 is log all.")
    args = parser.parse_args()

    filepath = args.filepath

    QUIET = args.quiet
    LOG = not QUIET and (args.log or (args.log_level != None))
    if args.log_level == None:
        LOG_LEVEL = -1 # Default log-level when only setting --log
    else:
        LOG_LEVEL = args.log_level

    if os.path.isfile(filepath):
        max_arbitrary_rect, max_strict_rect = solve(filepath)
        if not QUIET:
            print("a: %s is the maximal area of any rectangle spanned by two red tiles."%max_arbitrary_rect)
            print("b: %s is the maximal area of a rectangle of green tiles."%max_strict_rect)
        else:
            print(max_arbitrary_rect)
            print(max_strict_rect)
    else:
        print("There is no file '%s'"%filepath)
