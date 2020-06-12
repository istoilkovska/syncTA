# process local states
local = range(8)
# L states
L = {"x0" : [4], "x1" : [5], "f0" : [6], "f1" : [7], "v0" : [0, 2, 4, 6], "v1" : [1, 3, 5, 7], "corr0" : [0, 4], "corr1" : [1, 5]}
# initial states
initial = local

# rules
rules = []
rules.append({'idx': 0, 'from': 0, 'to': 0, 'guard': "(< x1 1)"})
rules.append({'idx': 1, 'from': 1, 'to': 0, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 2, 'from': 1, 'to': 1, 'guard': "(< x0 1)"})
rules.append({'idx': 3, 'from': 0, 'to': 1, 'guard': "(>= (+ x1 f1) 1)"})

rules.append({'idx': 4, 'from': 0, 'to': 4, 'guard': "(< x1 1)"})
rules.append({'idx': 5, 'from': 4, 'to': 0, 'guard': "(< x1 1)"})

rules.append({'idx': 6, 'from': 1, 'to': 4, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 7, 'from': 5, 'to': 0, 'guard': "(>= (+ x0 f0) 1)"})

rules.append({'idx': 8, 'from': 1, 'to': 5, 'guard': "(< x0 1)"})
rules.append({'idx': 9, 'from': 5, 'to': 1, 'guard': "(< x0 1)"})

rules.append({'idx': 10, 'from': 0, 'to': 5, 'guard': "(>= (+ x1 f1) 1)"})
rules.append({'idx': 11, 'from': 4, 'to': 1, 'guard': "(>= (+ x1 f1) 1)"})

rules.append({'idx': 12, 'from': 2, 'to': 2, 'guard': "(< x1 1)"})
rules.append({'idx': 13, 'from': 3, 'to': 2, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 14, 'from': 3, 'to': 3, 'guard': "(< x0 1)"})
rules.append({'idx': 15, 'from': 2, 'to': 3, 'guard': "(>= (+ x1 f1) 1)"})

rules.append({'idx': 16, 'from': 2, 'to': 6, 'guard': "(< x1 1)"})
rules.append({'idx': 17, 'from': 6, 'to': 2, 'guard': "(< x1 1)"})

rules.append({'idx': 18, 'from': 3, 'to': 6, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 19, 'from': 7, 'to': 2, 'guard': "(>= (+ x0 f0) 1)"})

rules.append({'idx': 20, 'from': 3, 'to': 7, 'guard': "(< x0 1)"})
rules.append({'idx': 21, 'from': 7, 'to': 3, 'guard': "(< x0 1)"})

rules.append({'idx': 22, 'from': 2, 'to': 7, 'guard': "(>= (+ x1 f1) 1)"})
rules.append({'idx': 23, 'from': 6, 'to': 3, 'guard': "(>= (+ x1 f1) 1)"})


# parameters, resilience condition
params = ["n", "t", "f"]
active = "n"
broadcast = [4, 5, 6, 7]
rc = ["(> n 0)", "(>= t 0)", "(>= t f)", "(> n t)"]

# faults
faults = "send omission"
faulty = [2, 3, 6, 7]
broadcast_faulty = [6, 7]
max_faulty = "f"
phase = 1

# rules disabled in clean round 
disabled_rules0 = [2, 8, 9, 13, 19, 20]
disabled_rules1 = [0, 4, 5, 12, 15, 16]

# configuration/transition constraints
constraints = []
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': local, 'result': active})
constraints.append({'type': 'configuration', 'sum': 'le', 'object': faulty, 'result': max_faulty})
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': broadcast, 'result': 1})
constraints.append({'type': 'transition', 'sum': 'eq', 'object': range(len(rules)), 'result': active})
constraints.append({'type': 'round_config', 'sum': 'eq', 'object': broadcast_faulty, 'result': 0})


properties = []
properties.append({'name':'validity0', 'spec':'safety', 'initial':'(= v0 0)', 'qf':'last', 'reachable':'(> corr0 0)'})
properties.append({'name':'validity1', 'spec':'safety', 'initial':'(= v1 0)', 'qf':'last', 'reachable':'(> corr1 0)'})
properties.append({'name':'agreement', 'spec':'safety', 'initial':'true', 'qf':'last', 'reachable':'(and (> corr0 0) (> corr1 0))'})
