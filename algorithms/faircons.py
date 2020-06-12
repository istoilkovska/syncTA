# process local states
local = range(11)
# L states
L = {"x0" : [0, 2, 3], "x1" : [1, 4], "cr0" : [5, 7, 8], "cr1" : [6, 9], "v0" : [0], "v1" : [1], "d0" : [2, 3], "d1" : [4]}
# initial states
initial = [0, 1, 5, 6]

# rules
rules = []
rules.append({'idx': 0, 'from': 0, 'to': 2, 'guard': "true"})
rules.append({'idx': 1, 'from': 1, 'to': 4, 'guard': "(< x0 1)"})
rules.append({'idx': 2, 'from': 1, 'to': 3, 'guard': "(>= (+ x0 cr0) 1)"})
rules.append({'idx': 3, 'from': 2, 'to': 2, 'guard': "true"})
rules.append({'idx': 4, 'from': 4, 'to': 4, 'guard': "(< x0 1)"})
rules.append({'idx': 5, 'from': 4, 'to': 3, 'guard': "(>= (+ x0 cr0) 1)"})
rules.append({'idx': 6, 'from': 3, 'to': 2, 'guard': "true"})
rules.append({'idx': 7, 'from': 0, 'to': 7, 'guard': "true"})
rules.append({'idx': 8, 'from': 1, 'to': 9, 'guard': "(< x0 1)"})
rules.append({'idx': 9, 'from': 1, 'to': 8, 'guard': "(>= (+ x0 cr0) 1)"})
rules.append({'idx': 10, 'from': 2, 'to': 7, 'guard': "true"})
rules.append({'idx': 11, 'from': 4, 'to': 9, 'guard': "(< x0 1)"})
rules.append({'idx': 12, 'from': 4, 'to': 8, 'guard': "(>= (+ x0 cr0) 1)"})
rules.append({'idx': 13, 'from': 3, 'to': 7, 'guard': "true"})
rules.append({'idx': 14, 'from': 5, 'to': 10, 'guard': "true"})
rules.append({'idx': 15, 'from': 6, 'to': 10, 'guard': "true"})
rules.append({'idx': 16, 'from': 7, 'to': 10, 'guard': "true"})
rules.append({'idx': 17, 'from': 8, 'to': 10, 'guard': "true"})
rules.append({'idx': 18, 'from': 9, 'to': 10, 'guard': "true"})
rules.append({'idx': 19, 'from': 10, 'to': 10, 'guard': "true"})

# parameters, resilience condition
params = ["n", "t", "f"]
active = "n"
rc = ["(> n 0)", "(>= t 0)", "(>= t f)", "(> n t)"]

# faults
faults = "crash"
faulty = [5, 6, 7, 8, 9, 10]
crashed = [3, 4, 5]
max_faulty = "f"
phase = 1

# configuration/transition constraints
constraints = []
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': local, 'result': active})
constraints.append({'type': 'configuration', 'sum': 'le', 'object': faulty, 'result': max_faulty})
constraints.append({'type': 'transition', 'sum': 'eq', 'object': range(len(rules)), 'result': active})
constraints.append({'type': 'round_config', 'sum': 'eq', 'object': crashed, 'result': 0})

properties = []
properties.append({'name':'validity0', 'spec':'safety', 'initial':'(= x0 n)', 'qf':'last', 'reachable':'(> d1 0)'})
properties.append({'name':'validity1', 'spec':'safety', 'initial':'(= x1 n)', 'qf':'last', 'reachable':'(> d0 0)'})
properties.append({'name':'agreement', 'spec':'safety', 'initial':'true', 'qf':'last', 'reachable':'(and (> d0 0) (> d1 0))'})
