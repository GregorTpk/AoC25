import os, sys, argparse
from multiprocessing import Pool

LOG = False
LOG_LEVEL = 0

HASH_BASE = 4
SUBPROCESSES = 7

def log(s="", log_level=None):
    if LOG and (LOG_LEVEL == -1 or (log_level != None and log_level <= LOG_LEVEL)): print(s)

class Hashtable:
    def __init__(self, indicator_count):
        self.indicator_count = indicator_count

        self.tbl = [[] for i in range(HASH_BASE**indicator_count)]

        self.entry_count = 0
    def retrieve(self, joltage_values):
        """Returns JoltageValues-object whose joltage matches joltage_values if it exists,
        None otherwise."""
        for candidate in self.tbl[joltage_values.hash]:
            if candidate.joltage == joltage_values.joltage:
                return candidate

        return None
    def add_new(self, joltage_values):
        """Adds button_presses without checking if matching object already contained."""
        self.entry_count += 1
        self.tbl[joltage_values.hash].append(joltage_values)
    def remove(self, joltage_values):
        """Removes joltage_values from hashtable"""
        self.entry_count -= 1
        self.tbl[joltage_values.hash].remove(joltage_values)

class JoltageButtonPresses:
    def __init__(self, press_count, press_list):
        self.press_count = press_count
        self.press_list = press_list

class JoltageValues:
    def __init__(self, machine, button_presses=None, joltage=None):
        self.machine = machine

        if button_presses == None:
            button_presses = JoltageButtonPresses(0, [0]*len(machine.buttons))
        self.button_presses = button_presses

        if joltage == None:
            joltage = [0] * len(machine.joltage_requirements)
        self.joltage = joltage
        self.lowest_required_joltage = None
        self.lowest_required_joltage_indices = None
        self.hash = None

        self.calculate_hash()
        self.find_lowest_required_joltage()
    def __repr__(self):
        return "JV%s(%s presses)%s"%(self.joltage, self.button_presses.press_count, self.button_presses.press_list)
    def find_lowest_required_joltage(self):
        min_req_jolt = None
        min_req_jolt_indices = None
        for i, (req_jolt, jolt) in enumerate(zip(self.machine.joltage_requirements, self.joltage)):
            if req_jolt - jolt > 0:
                if min_req_jolt == None or jolt < min_req_jolt:
                    min_req_jolt = jolt
                    min_req_jolt_indices = [i]
                elif jolt == min_req_jolt:
                    min_req_jolt_indices.append(i)
        self.lowest_required_joltage = min_req_jolt
        self.lowest_required_joltage_indices = min_req_jolt_indices
    def calculate_hash(self):
        self.hash = sum(((j % HASH_BASE) * HASH_BASE**i for i, j in enumerate(self.joltage)))

class Machine:
    def __init__(self, indicator_diagram, buttons, joltage_requirements):
        self.indicator_button_presses = None
        self.indicator_diagram = indicator_diagram

        self.buttons = buttons

        self.joltage_requirements = joltage_requirements
        self.joltage_solution = None
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
        ht = Hashtable(len(self.joltage_requirements))

        current_lowest_joltage = 0
        zero_joltage_values = JoltageValues(self)
        joltage_values_fronts = [[zero_joltage_values]]

        ht.add_new(zero_joltage_values)

        while joltage_values_fronts:
            log("Currently at lowest joltage of %s"%current_lowest_joltage, 2)
            front = joltage_values_fronts[0]
            for jolt_values in front:
                log(jolt_values, 3)
                log("Hash %s"%jolt_values.hash, 4)
                log("Current front size %s"%len(front), 4)
                log("Hashtable size %s"%ht.entry_count)
                log("Hashtable entry size %s"%len(ht.tbl[jolt_values.hash]), 4)
                for button_idx, button in enumerate(self.buttons):
                    for jolt_idx in jolt_values.lowest_required_joltage_indices:
                        #Button connected to lowest required joltage
                        if jolt_idx in button:
                            #Try to press button
                            valid = True
                            new_joltage = jolt_values.joltage[:]
                            for connected_joltage in button:
                                new_joltage[connected_joltage] += 1
                                if new_joltage[connected_joltage] > self.joltage_requirements[connected_joltage]:
                                    valid = False
                                    break
                            #Press button
                            if valid:
                                button_presses = jolt_values.button_presses
                                new_press_count = button_presses.press_count + 1
                                new_press_list = button_presses.press_list[:]
                                new_press_list[button_idx] += 1
                                new_button_presses = JoltageButtonPresses(new_press_count, new_press_list)

                                new_jolt_values = JoltageValues(self, new_button_presses, new_joltage)

                                ht_entry = ht.retrieve(new_jolt_values)

                                #Joltage values not yet in hashtable
                                if ht_entry == None:
                                    #Add to hashtable
                                    ht.add_new(new_jolt_values)
                                    #Add to front to expand if there is required joltage left
                                    if new_jolt_values.lowest_required_joltage != None:
                                        front_idx = new_jolt_values.lowest_required_joltage - current_lowest_joltage
                                        for new_front in range(front_idx + 1 - len(joltage_values_fronts)):
                                            joltage_values_fronts.append([])
                                        joltage_values_fronts[front_idx].append(new_jolt_values)
                                    else:
                                        self.joltage_solution = new_jolt_values
                                #Joltage values already in hashtable
                                elif ht_entry.button_presses.press_count > new_press_count:
                                    #Improvement in press_count
                                    ht_entry.button_presses = new_button_presses
                            break
                ht.remove(jolt_values)
            current_lowest_joltage += 1
            joltage_values_fronts.pop(0)
        log(self.joltage_solution.joltage, 3)
        log(self.joltage_solution.button_presses.press_count, 2)
        log(self.joltage_solution.button_presses.press_list, 3)

def solve_machine(pair):
    i, m = pair
    m.set_joltage()
    print("Finished machine %s with %s presses"%(i+1, m.joltage_solution.button_presses.press_count))
    return m.joltage_solution.button_presses.press_count

def solve(filepath):
    log("Reading file", 0)
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

    log("Setting up data structure", 0)

    min_total_indicator_presses = 0
    for m in []:#machines:
        m.set_indicators()

        min_total_indicator_presses += sum(m.indicator_button_presses)

    log("Finished with indicators!", 0)

    min_total_joltage_presses = 0

    for i, m in enumerate(machines):
        min_total_joltage_presses += solve_machine((i, m))

#    with Pool(SUBPROCESSES) as p:
#        min_total_joltage_presses = sum(p.map(solve_machine, enumerate(machines)))

#    for i, m in enumerate(machines):
#        log("Set joltage of machine %s"%i, 1)
#        m.set_joltage()
#
#        min_total_joltage_presses += m.joltage_solution.button_presses.press_count

    log("Finished with joltage!", 0)

    for m in machines:
        print(m.buttons)
        print(m.joltage_requirements)
        #print(m.joltage_solution.button_presses.press_list)
        print()

    return min_total_indicator_presses, min_total_joltage_presses

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
