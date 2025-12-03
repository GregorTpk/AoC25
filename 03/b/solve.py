import os, sys

ACTIVATED_BATTERIES_PER_BANK = 12

#Key for max-function: take first occurence of highest joltage
key_func = lambda idx_joltage_pair: idx_joltage_pair[1]

def solve(filepath):

    banks = None
    with open(filepath, "r") as f:
        banks = [[int(digit) for digit in line.strip()] for line in f.readlines()]

    joltage_sum = 0

    if banks != None:
        for bank in banks:

            #List of joltages
            activated_battery_joltages = []
            #Index of the last added battery
            idx = -1
            for i in range(ACTIVATED_BATTERIES_PER_BANK):
                eligible_batteries = bank[idx + 1 : len(bank) - ACTIVATED_BATTERIES_PER_BANK + i + 1]

                #Find first occurence of highest joltage in eligible interval
                idx_step, jolt = max(enumerate(eligible_batteries), key=key_func)

                activated_battery_joltages.append(jolt)
                idx += idx_step+1

            #Calculate total joltage in current block
            joltage = sum([jolt * 10**(ACTIVATED_BATTERIES_PER_BANK-idx-1) for idx, jolt in enumerate(activated_battery_joltages)])
            joltage_sum += joltage

    return joltage_sum

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
