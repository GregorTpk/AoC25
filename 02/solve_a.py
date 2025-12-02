import os, sys

def get_closest_half(svalue, ivalue, comp, default_if_odd):
    """Returns the half-number closest to ivalue as a string.
    comp == 1 returns minimal larger number, comp == -1 returns maximal smaller number.
    default_if_odd(l) returns the default for ivalue having odd length l"""
    if len(svalue) % 2 == 0:
        sclosest_half = svalue[:len(svalue)//2]

        if comp*int(sclosest_half * 2) < comp*ivalue:
            sclosest_half = str(int(sclosest_half) + comp)
    else:
        sclosest_half = default_if_odd(len(svalue))
    return sclosest_half

def solve(filepath):
    invalid_half_ids = []
    spairs = None

    with open(filepath, "r") as f:
        spairs = [p.split("-") for p in f.read().strip().split(",")]
        ipairs = [(int(p0), int(p1)) for p0, p1 in spairs]

    if spairs != None:
        for spair, ipair in zip(spairs, ipairs):
            slower_half = get_closest_half(spair[0], ipair[0], comp=1,
                                           default_if_odd=lambda l: str(10**(len(spair[0])//2)))

            supper_half = get_closest_half(spair[1], ipair[1], comp=-1,
                                           default_if_odd=lambda l: str(10**(len(spair[1])//2) - 1))

            invalid_half_ids += range(int(slower_half), int(supper_half)+1)

    #Sum over all invalid ids
    invalid_id_sum = 0
    for invalid_half in invalid_half_ids:
        invalid_id_sum += int(2*str(invalid_half))

    return invalid_id_sum, None

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        filepath = "input.txt"

    if os.path.isfile(filepath):
        results = solve(filepath)

        print("Result 1: ", results[0])
        print("Result 2: ", results[1])
    else:
        print("There is no such file")
