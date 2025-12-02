import os

# inputs are in <input.txt>
os.chdir('AoC25/1/a')
input = open("input.txt").read().strip().split("\n")

# Constants and Variables
START_POSITION = 50
LENGTH = 100 # -> N mod 100
DIRECTION = {"L": -1, "R": 1}

position = START_POSITION
counter_pass_zero = 0
counter_lands_zero = 0

for i in range(len(input)):
    # compute position after move
    direction = DIRECTION[input[i][0]]
    step = int(input[i][1:])

    full_revolutions = step // LENGTH
    remainder_steps = step % LENGTH

    if position != 0 and (position + direction * remainder_steps < 0 or position + direction * remainder_steps > LENGTH):
        counter_pass_zero += 1
    
    counter_pass_zero = counter_pass_zero + full_revolutions

    new_position = (position + direction * remainder_steps) % LENGTH

    # lands on zero
    if new_position == 0:
        counter_lands_zero = counter_lands_zero + 1
    
    position = new_position

print(counter_lands_zero)
print(counter_pass_zero)

print("Total zero or past zero: ", counter_lands_zero + counter_pass_zero)