import os
import re

# 1. Compute all numbers in the range
# 2. For each number in the range, get number of possible substrings (= get divisors of length of string)
# 3. For each divisor, get all substrings of that length
# 4. Check if number is made up of repeated substrings
# 5. If TRUE, add to invalid_id list

#os.getcwd
input = open("02/input.txt").read()
input = re.split(",|\n", input)

invalid_id = list()

def get_divisors(n):
    divisors = []
    for i in range(1, n + 1):
        if n % i == 0 and i != n:
            divisors.append(i)
    return divisors

for i in range(len(input)): # get all numbers in range
    start = int(input[i].split('-')[0])
    end = int(input[i].split('-')[1]) + 1
    all_num = list(range(start, end))
    for j in range(len(all_num)): # for each number in range, get all divisors of the length of the string
       length_of_num = len(str(all_num[j]))
       for k in range(len(get_divisors(length_of_num))):
           substring = str(all_num[j])[:get_divisors(length_of_num)[k]]
           if substring * (length_of_num // get_divisors(length_of_num)[k]) == str(all_num[j]):
               invalid_id.append(all_num[j])

# numbers are twice in invaldi_id:
invalid_id = set(invalid_id)

print(sum(invalid_id))