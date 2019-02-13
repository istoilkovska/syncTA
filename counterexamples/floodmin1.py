# process local states
local = range(5)
# L states
L = {"x0" : [0], "x1" : [1], "cr0" : [2], "cr1" : [3], "v0" : [0, 2], "v1" : [1, 3]}
# initial states
initial = [0, 1, 2, 3]

# rules
rules = []
rules.append({'idx': 0, 'from': 0, 'to': 0, 'guard': "true"})
rules.append({'idx': 1, 'from': 1, 'to': 0, 'guard': "(>= (+ x0 cr0) 1)"})
rules.append({'idx': 2, 'from': 1, 'to': 1, 'guard': "(< x0 1)"})
rules.append({'idx': 3, 'from': 0, 'to': 2, 'guard': "true"})
rules.append({'idx': 4, 'from': 1, 'to': 2, 'guard': "(>= (+ x0 cr0) 1)"})
rules.append({'idx': 5, 'from': 1, 'to': 3, 'guard': "(< x0 1)"})
rules.append({'idx': 6, 'from': 2, 'to': 4, 'guard': "true"})
rules.append({'idx': 7, 'from': 3, 'to': 4, 'guard': "true"})
rules.append({'idx': 8, 'from': 4, 'to': 4, 'guard': "true"})

# parameters, resilience condition
params = ["n", "t", "f"]
active = "n"
rc = ["(> n 0)", "(>= t 0)", "(>= t f)", "(> n t)"]

# faults
faults = "crash"
faulty = [2, 3, 4]
crashed = [2, 3]
max_faulty = "f"
phase = 1

# configuration/transition constraints
constraints = []
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': local, 'result': active})
constraints.append({'type': 'configuration', 'sum': 'le', 'object': faulty, 'result': max_faulty})
constraints.append({'type': 'transition', 'sum': 'eq', 'object': range(len(rules)), 'result': active})
# CLEAN ROUND CONSTRAINT OMITTED

properties = []
properties.append({'name':'validity0', 'spec':'safety', 'initial':'(= v0 0)', 'qf':'last', 'reachable':'(> x0 0)'})
properties.append({'name':'validity1', 'spec':'safety', 'initial':'(= v1 0)', 'qf':'last', 'reachable':'(> x1 0)'})
properties.append({'name':'agreement', 'spec':'safety', 'initial':'true', 'qf':'last', 'reachable':'(and (> x0 0) (> x1 0))'})
