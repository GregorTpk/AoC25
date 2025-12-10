import os, sys

class Machine:
    def __init__(self, indicator_diagram, buttons, joltage_requirements):
        self.indicator_button_presses = None
        self.indicator_diagram = indicator_diagram

        self.buttons = buttons

        self.joltage_presses = None
        self.joltage_requirements = joltage_requirements

        self.__joltage_min_presses_count_upperbound = None
        self.__joltage_solution = None
    def set_indicators(self):
        min_sol_presses = None
        min_solution = None
        for solution_idx in range(2**len(self.buttons)):
            button_presses = [1 & solution_idx >> i for i in range(len(self.buttons))]
            indicators = [False] * len(self.indicator_diagram)
            for button, pressed in zip(self.buttons, button_presses):
                if pressed:
                    for connected_indicator in button:
                        indicators[connected_indicator] = not indicators[connected_indicator]
            if indicators == self.indicator_diagram and (min_sol_presses == None or min_sol_presses > sum(button_presses)):
                min_sol_presses = sum(button_presses)
                min_solution = button_presses
        self.indicator_button_presses = min_solution
    def set_joltage(self):
        def set_joltage_rec(first_button_idx, seq, remaining_joltage):
#            print("seq is %s"%seq)
#            print("rem jolt is %s"%remaining_joltage)
#            print("min_upperbound is %s"%self.__joltage_min_presses_count_upperbound)
#            print("solution %s"%self.__joltage_solution)
            for idx, button in enumerate(self.buttons[first_button_idx:], start=first_button_idx):
                new_remaining_joltage = remaining_joltage[:]
                invalid_button_press = False
#                print("Apply button %s, %s"%(idx, button))
                for incr_idx in button:
                    new_remaining_joltage[incr_idx] -= 1

                    #Overshot joltage, invalid button press
                    if new_remaining_joltage[incr_idx] < 0:
                        invalid_button_press = True
                        break

                if invalid_button_press:
                    continue

                new_seq = seq[:]
                new_seq.append(idx)

                #Correct joltage
                remaining_joltage_sum = sum(new_remaining_joltage)
                if remaining_joltage_sum == 0:
                    print("yes")
                    #Assert: improvement in press count
                    self.__joltage_min_presses_count_upperbound = len(new_seq)
                    self.__joltage_solution = new_seq
                    return

                #Optimistic estimation
                optimistic_joltage_reduction = len(self.buttons[idx]) * (self.__joltage_min_presses_count_upperbound-1 - len(new_seq))

                #Bound search tree
                if len(new_seq) < self.__joltage_min_presses_count_upperbound - 1:
                    if optimistic_joltage_reduction >= remaining_joltage_sum:
                        set_joltage_rec(idx, new_seq, new_remaining_joltage)
                    else:
                        print("reduction through optimistic estimation")

        #Set some initial upperbound
        self.__joltage_min_presses_count_upperbound = sum(self.joltage_requirements) + 1

        #Start recursion
        set_joltage_rec(0, [], self.joltage_requirements)

        self.joltage_presses = self.__joltage_solution
        print(self.joltage_requirements)
        print(self.buttons)
        print(self.joltage_presses)
        print(self.__joltage_min_presses_count_upperbound)
        print()

def solve(filepath):
    with open(filepath, "r") as f:
        machines = []
        for line in f.readlines():
            descr = line.strip().split(" ")
            ind_diag = [False if char == "." else True for char in descr[0][1:-1]]
            sort_key = lambda button: len(button)
            buttons = sorted(([int(ind_idx) for ind_idx in button[1:-1].split(",")] for button in descr[1:-1]), key=sort_key, reverse=True)
            print(buttons)
            jolt_req = [int(jolt) for jolt in descr[-1][1:-1].split(",")]
            machines.append(Machine(ind_diag, buttons, jolt_req))

    min_total_indicator_presses = 0
    for m in []:#machines:
        m.set_indicators()

        min_total_indicator_presses += sum(m.indicator_button_presses)

    print("Finished with indicators!")

    min_total_joltage_presses = 0
    for m in machines:
        m.set_joltage()

        min_total_joltage_presses += len(m.joltage_presses)

    print("Finished with joltage!")

    for m in machines:
        print(m.buttons)
        print(m.joltage_requirements)
        print(m.joltage_presses)
        print()

    return min_total_indicator_presses, min_total_joltage_presses


if __name__ == "__main__":
    (filepath := sys.argv[1]) if len(sys.argv) >= 2 else (filepath := "input.txt")
    print(solve(filepath)) if os.path.isfile(filepath) else print("There is no such file")
