# process local states
local = range(6)
# L states
L = {"x0" : [0], "x1" : [1], "x2" : [2], "f0" : [3], "f1" : [4], "f2" : [5], "v0" : [0, 3], "v1" : [1, 4], "v2" : [2, 5]}
# initial states
initial = [0, 1, 2, 3, 4, 5]

# rules
rules = []
rules.append({'idx': 0, 'from': 0, 'to': 0, 'guard': "true"})
rules.append({'idx': 1, 'from': 1, 'to': 0, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 2, 'from': 1, 'to': 1, 'guard': "(< x0 1)"})
rules.append({'idx': 3, 'from': 2, 'to': 0, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 4, 'from': 2, 'to': 1, 'guard': "(and (>= (+ x1 f1) 1) (< x0 1))"})
rules.append({'idx': 5, 'from': 2, 'to': 2, 'guard': "(and (< x0 1) (< x1 1))"})

rules.append({'idx': 6, 'from': 3, 'to': 3, 'guard': "true"})
rules.append({'idx': 7, 'from': 4, 'to': 3, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 8, 'from': 4, 'to': 4, 'guard': "(< x0 1)"})
rules.append({'idx': 9, 'from': 5, 'to': 3, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 10, 'from': 5, 'to': 4, 'guard': "(and (>= (+ x1 f1) 1) (< x0 1))"})
rules.append({'idx': 11, 'from': 5, 'to': 5, 'guard': "(and (< x0 1) (< x1 1))"})

# parameters, resilience condition
params = ["n", "t", "f"]
active = "n"
rc = ["(> n 0)", "(>= t 0)", "(>= t f)", "(> n t)"]

# faults
faults = "send omission"
faulty = [3, 4, 5]
max_faulty = "f"
phase = 1

# rules disabled in clean round 
disabled_rules0 = [2, 5, 8, 11]
disabled_rules1 = [5, 11]

# configuration/transition constraints
constraints = []
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': local, 'result': active})
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': faulty, 'result': max_faulty})
constraints.append({'type': 'transition', 'sum': 'eq', 'object': range(len(rules)), 'result': active})
constraints.append({'type': 'round_trans', 'pre': '(>= (+ x0 f0) 1)', 'sum': 'eq', 'object': disabled_rules0, 'result': 0})
constraints.append({'type': 'round_trans', 'pre': '(>= (+ x1 f1) 1)', 'sum': 'eq', 'object': disabled_rules1, 'result': 0})

properties = []
properties.append({'name':'validity0', 'spec':'safety', 'initial':'(= v0 0)', 'qf':'last', 'reachable':'(> x0 0)'})
properties.append({'name':'validity1', 'spec':'safety', 'initial':'(= v1 0)', 'qf':'last', 'reachable':'(> x1 0)'})
properties.append({'name':'validity2', 'spec':'safety', 'initial':'(= v2 0)', 'qf':'last', 'reachable':'(> x2 0)'})
properties.append({'name':'agreement', 'spec':'safety', 'initial':'true', 'qf':'last', 'reachable':'(and (> x0 0) (> x1 0) (> x2 0))'})