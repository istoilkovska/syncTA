# process local states
local = range(7)
# L states
L = {"x0" : [0, 2], "x1" : [1, 2], "cr0" : [3, 5], "cr1" : [4, 5], "v0" : [0, 3], "v1" : [1, 4], "d0" : [0, 2], "d1" : [1]}
# initial states
initial = [0, 1, 3, 4]

# rules
rules = []
rules.append({'idx': 0, 'from': 0, 'to': 0, 'guard': "(< x1 1)"})
rules.append({'idx': 1, 'from': 0, 'to': 2, 'guard': "(>= (+ x1 cr1) 1)"})
rules.append({'idx': 2, 'from': 2, 'to': 2, 'guard': "true"})
rules.append({'idx': 3, 'from': 1, 'to': 2, 'guard': "(>= (+ x0 cr0) 1)"})
rules.append({'idx': 4, 'from': 1, 'to': 1, 'guard': "(< x0 1)"})
rules.append({'idx': 5, 'from': 0, 'to': 3, 'guard': "(< x1 1)"})
rules.append({'idx': 6, 'from': 0, 'to': 5, 'guard': "(>= (+ x1 cr1) 1)"})
rules.append({'idx': 7, 'from': 2, 'to': 5, 'guard': "true"})
rules.append({'idx': 8, 'from': 1, 'to': 5, 'guard': "(>= (+ x0 cr0) 1)"})
rules.append({'idx': 9, 'from': 1, 'to': 4, 'guard': "(< x0 1)"})
rules.append({'idx': 10, 'from': 3, 'to': 6, 'guard': "true"})
rules.append({'idx': 11, 'from': 5, 'to': 6, 'guard': "true"})
rules.append({'idx': 12, 'from': 4, 'to': 6, 'guard': "true"})
rules.append({'idx': 13, 'from': 6, 'to': 6, 'guard': "true"})

# parameters, resilience condition
params = ["n", "t", "f"]
active = "n"
rc = ["(> n 0)", "(>= t 0)", "(>= t f)", "(> n t)"]

# faults
faults = "crash"
faulty = [3, 4, 5, 6]
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
properties.append({'name':'validity0', 'spec':'safety', 'initial':'(= v0 n)', 'qf':'last', 'reachable':'(> d1 0)'})
properties.append({'name':'validity1', 'spec':'safety', 'initial':'(= v1 n)', 'qf':'last', 'reachable':'(> d0 0)'})
properties.append({'name':'agreement', 'spec':'safety', 'initial':'true', 'qf':'last', 'reachable':'(and (> d0 0) (> d1 0))'})
