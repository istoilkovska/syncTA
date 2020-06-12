# process local states
local = range(12)
# L states
L = {"x0" : [6], "x1" : [7], "x2" : [8],
     "f0" : [9], "f1" : [10], "f2" : [11],
     "v0" : [0, 3, 6, 9], "v1" : [1, 4, 7, 10], "v2" : [2, 5, 8, 11],
     "corr0" : [0, 6], "corr1" : [1, 7], "corr2" : [2, 8]}
# initial states
initial = local

# rules
rules = []
rules.append({'idx': 0, 'from': 0, 'to': 0, 'guard': "(and (< x1 1) (< x2 1))"})
rules.append({'idx': 1, 'from': 0, 'to': 1, 'guard': "(>= (+ x1 f1) 1)"})
rules.append({'idx': 2, 'from': 0, 'to': 2, 'guard': "(>= (+ x2 f2) 1)"})

rules.append({'idx': 3, 'from': 1, 'to': 1, 'guard': "(and (< x0 1) (< x2 1))"})
rules.append({'idx': 4, 'from': 1, 'to': 0, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 5, 'from': 1, 'to': 2, 'guard': "(>= (+ x2 f2) 1)"})

rules.append({'idx': 6, 'from': 2, 'to': 2, 'guard': "(and (< x0 1) (< x1 1))"})
rules.append({'idx': 7, 'from': 2, 'to': 0, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 8, 'from': 2, 'to': 1, 'guard': "(>= (+ x1 f1) 1)"})

rules.append({'idx': 9, 'from': 0, 'to': 6, 'guard': "(and (< x1 1) (< x2 1))"})
rules.append({'idx': 10, 'from': 0, 'to': 7, 'guard': "(>= (+ x1 f1) 1)"})
rules.append({'idx': 11, 'from': 0, 'to': 8, 'guard': "(>= (+ x2 f2) 1)"})

rules.append({'idx': 12, 'from': 1, 'to': 7, 'guard': "(and (< x0 1) (< x2 1))"})
rules.append({'idx': 13, 'from': 1, 'to': 6, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 14, 'from': 1, 'to': 8, 'guard': "(>= (+ x2 f2) 1)"})

rules.append({'idx': 15, 'from': 2, 'to': 8, 'guard': "(and (< x0 1) (< x1 1))"})
rules.append({'idx': 16, 'from': 2, 'to': 6, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 17, 'from': 2, 'to': 7, 'guard': "(>= (+ x1 f1) 1)"})

rules.append({'idx': 18, 'from': 6, 'to': 0, 'guard': "(and (< x1 1) (< x2 1))"})
rules.append({'idx': 19, 'from': 6, 'to': 1, 'guard': "(>= (+ x1 f1) 1)"})
rules.append({'idx': 20, 'from': 6, 'to': 2, 'guard': "(>= (+ x2 f2) 1)"})

rules.append({'idx': 21, 'from': 7, 'to': 1, 'guard': "(and (< x0 1) (< x2 1))"})
rules.append({'idx': 22, 'from': 7, 'to': 0, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 23, 'from': 7, 'to': 2, 'guard': "(>= (+ x2 f2) 1)"})

rules.append({'idx': 24, 'from': 8, 'to': 2, 'guard': "(and (< x0 1) (< x1 1))"})
rules.append({'idx': 25, 'from': 8, 'to': 0, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 26, 'from': 8, 'to': 1, 'guard': "(>= (+ x1 f1) 1)"})


# send omission faulty
rules.append({'idx': 27, 'from': 3, 'to': 3, 'guard': "(and (< x1 1) (< x2 1))"})
rules.append({'idx': 28, 'from': 3, 'to': 4, 'guard': "(>= (+ x1 f1) 1)"})
rules.append({'idx': 29, 'from': 3, 'to': 5, 'guard': "(>= (+ x2 f2) 1)"})

rules.append({'idx': 30, 'from': 4, 'to': 4, 'guard': "(and (< x0 1) (< x2 1))"})
rules.append({'idx': 31, 'from': 4, 'to': 3, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 32, 'from': 4, 'to': 5, 'guard': "(>= (+ x2 f2) 1)"})

rules.append({'idx': 33, 'from': 5, 'to': 5, 'guard': "(and (< x0 1) (< x1 1))"})
rules.append({'idx': 34, 'from': 5, 'to': 3, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 35, 'from': 5, 'to': 4, 'guard': "(>= (+ x1 f1) 1)"})

rules.append({'idx': 36, 'from': 3, 'to': 9, 'guard': "(and (< x1 1) (< x2 1))"})
rules.append({'idx': 37, 'from': 3, 'to': 10, 'guard': "(>= (+ x1 f1) 1)"})
rules.append({'idx': 38, 'from': 3, 'to': 11, 'guard': "(>= (+ x2 f2) 1)"})

rules.append({'idx': 39, 'from': 4, 'to': 10, 'guard': "(and (< x0 1) (< x2 1))"})
rules.append({'idx': 40, 'from': 4, 'to': 9, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 41, 'from': 4, 'to': 11, 'guard': "(>= (+ x2 f2) 1)"})

rules.append({'idx': 42, 'from': 5, 'to': 11, 'guard': "(and (< x0 1) (< x1 1))"})
rules.append({'idx': 43, 'from': 5, 'to': 9, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 44, 'from': 5, 'to': 10, 'guard': "(>= (+ x1 f1) 1)"})

rules.append({'idx': 45, 'from': 9, 'to': 3, 'guard': "(and (< x1 1) (< x2 1))"})
rules.append({'idx': 46, 'from': 9, 'to': 4, 'guard': "(>= (+ x1 f1) 1)"})
rules.append({'idx': 47, 'from': 9, 'to': 5, 'guard': "(>= (+ x2 f2) 1)"})

rules.append({'idx': 48, 'from': 10, 'to': 4, 'guard': "(and (< x0 1) (< x2 1))"})
rules.append({'idx': 49, 'from': 10, 'to': 3, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 50, 'from': 10, 'to': 5, 'guard': "(>= (+ x2 f2) 1)"})

rules.append({'idx': 51, 'from': 11, 'to': 5, 'guard': "(and (< x0 1) (< x1 1))"})
rules.append({'idx': 52, 'from': 11, 'to': 3, 'guard': "(>= (+ x0 f0) 1)"})
rules.append({'idx': 53, 'from': 11, 'to': 4, 'guard': "(>= (+ x1 f1) 1)"})


# parameters, resilience condition
params = ["n", "t", "f"]
active = "n"
broadcast = [6, 7, 8, 9, 10, 11]
rc = ["(> n 0)", "(>= t 0)", "(>= t f)", "(> n t)"]

# faults
faults = "send omission"
faulty = [3, 4, 5, 9, 10, 11]
broadcast_faulty = [9, 10, 11]
max_faulty = "f"
phase = 1

# configuration/transition constraints
constraints = []
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': local, 'result': active})
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': faulty, 'result': max_faulty})
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': broadcast, 'result': 2})
constraints.append({'type': 'transition', 'sum': 'eq', 'object': range(len(rules)), 'result': active})
constraints.append({'type': 'round_config', 'sum': 'le', 'object': broadcast_faulty, 'result': 1})


properties = []
properties.append({'name':'validity0', 'spec':'safety', 'initial':'(= v0 0)', 'qf':'last', 'reachable':'(> corr0 0)'})
properties.append({'name':'validity1', 'spec':'safety', 'initial':'(= v1 0)', 'qf':'last', 'reachable':'(> corr1 0)'})
properties.append({'name':'agreement', 'spec':'safety', 'initial':'true', 'qf':'last', 'reachable':'(and (> corr0 0) (> corr1 0) (> corr2 0))'})
