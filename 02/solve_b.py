import os, sys

def get_divisors(n):
    return filter(lambda candidate: n % candidate == 0,
                  range(1, n//2 + 1))

def get_invalid_id(pattern, repetitions):
    return int(str(pattern)*repetitions)

def is_primitive_pattern(spattern):
    #Determine whether pattern can be written as a repetition of a smaller pattern
    for subpattern_length in get_divisors(len(spattern)):
        if spattern[:subpattern_length] * (len(spattern) // subpattern_length) == spattern:
            return False

    return True

def solve(filepath):
    invalid_ids = []
    spairs = None

    with open(filepath, "r") as f:
        spairs = [p.split("-") for p in f.read().strip().split(",")]
        ipairs = [(int(p0), int(p1)) for p0, p1 in spairs]

    if spairs != None:
        for spair, ipair in zip(spairs, ipairs):

            #Treat each id-length in the intervall individually
            for id_length in range(len(spair[0]), len(spair[1])+1):
                for pattern_length in get_divisors(id_length):
                    repetitions = id_length // pattern_length

                    if id_length == len(spair[0]):
                        pattern_lower_bound = int(spair[0][:pattern_length])

                        if get_invalid_id(pattern_lower_bound, repetitions) < ipair[0]:
                            pattern_lower_bound += 1
                    else:
                        pattern_lower_bound = 10**(pattern_length - 1)

                    if id_length == len(spair[1]):
                        pattern_upper_bound = int(spair[1][:pattern_length])

                        if get_invalid_id(pattern_upper_bound, repetitions) > ipair[1]:
                            pattern_upper_bound -= 1
                    else:
                        pattern_upper_bound = 10**pattern_length - 1

                    for pattern in range(pattern_lower_bound, pattern_upper_bound+1):
                        if is_primitive_pattern(str(pattern)):
                            inv_id = get_invalid_id(pattern, repetitions)
                            invalid_ids.append(inv_id)

    return sum(invalid_ids)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        filepath = "input.txt"

    if os.path.isfile(filepath):
        result = solve(filepath)

        print(result)
    else:
        print("There is no such file")
