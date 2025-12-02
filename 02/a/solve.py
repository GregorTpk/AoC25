import os
import re

os.getcwd
input = open("02/input.txt").read()
input = re.split(",|\n", input)

invalid_id = list()

for i in range(len(input)):
    start = int(input[i].split('-')[0])
    end = int(input[i].split('-')[1]) + 1
    all_num = list(range(start, end))
    for j in range(len(all_num)):
        if len(str(all_num[j]))/2 == len(str(all_num[j]))//2:
            if str(all_num[j])[:(len(str(all_num[j]))//2)] == str(all_num[j])[(len(str(all_num[j]))//2):]:
                invalid_id.append(all_num[j])

print(invalid_id)
print(sum(invalid_id))