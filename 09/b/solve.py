import os, sys

def binary_search(column, y):
    #Returns idx of first vertical edge above or at y if it exists, None otherwise

    a = 0
    b = len(column) - 1

    #TODO: out of interval

    while a < b:
        c = (a + b + 1) // 2
        if column[c] <= y:
            a = c
        else:
            b = c-1

    if a == b and column[a] <= y:
        return a

    return None

def solve(filepath):
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

    width += 1
    height += 1
    print(width)
    print(height)
    #Construct edges
    #For each global column: store vertical edges in this column
    horizontal_edges = [[] for i in range(width)]
    vertical_edges = [[] for i in range(width)]

    for i, tile2 in enumerate(tiles):
        tile1 = tiles[i-1]
        #Only consider vertical edges
        if tile1[1] == tile2[1]:
            print(tile1)
            print(tile2)
            y = tile1[1]
            left_corner, right_corner = sorted((tile1[0], tile2[0]))
            for x in range(left_corner, right_corner+1):
                horizontal_edges[x].append(y)

        if tile1[0] == tile2[0]:
            x = tile1[0]
            up_corner, down_corner = sorted((tile1[1], tile2[1]))
            for y in range(up_corner, down_corner+1):
                vertical_edges[x].append(y)


    #Sort all vertical-edge collections
    for column in horizontal_edges:
        column.sort()
    for column in vertical_edges:
        column.sort()

    def check_tile(x, y):
        v_edge_idx = binary_search(vertical_edges[x], y)
        h_edge_idx = binary_search(horizontal_edges[x], y)
        if v_edge_idx != None or (h_edge_idx != None and (horizontal_edges[x][h_edge_idx] == y or h_edge_idx % 2 == 0)):
                return True
        return False

    max_area = 0

    for i, p1 in enumerate(tiles):
        for p2 in tiles[i+1:]:
            area = ((abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1))

            if area > max_area:
                #Iterate over horizontal edges of rectangle
                #print("Checking %s, %s"%(p1, p2))
                fail = False
                for y in (p1[1], p2[1]):
                    left, right = sorted((p1[0], p2[0]))
                    for x in range(left, right+1):
                        if not check_tile(x, y):
                            fail = True
                            break
                    if fail:
                        break
                if fail:
                    continue

                #Iterate over vertical edges of rectangle
                for x in (p1[0], p2[0]):
                    up, down = sorted((p1[1], p2[1]))
                    for y in range(up, down+1):
                        if not check_tile(x, y):
                            fail = True
                            break
                    if fail:
                        break
                if fail:
                    continue
                print("Successful!")
                print("Tiles %s, %s"%(p1, p2))
                print(area)

                max_area = area


    return max_area

if __name__ == "__main__":
    (filepath := sys.argv[1]) if len(sys.argv) >= 2 else (filepath := "input.txt")
    print(solve(filepath)) if os.path.isfile(filepath) else print("There is no such file")
