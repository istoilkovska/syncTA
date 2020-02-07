# process local states
local = range(4)
# L states
L = {"x":[1, 2, 3], "v1":[1], "acc":[3]}
# initial states
initial = [0, 1]

# rules
rules = []
rules.append({'idx': 0, 'from': 0, 'to': 0, 'guard': "(< x (+ t 1))"})
rules.append({'idx': 1, 'from': 0, 'to': 2, 'guard': "(>= (+ x f) (+ t 1))"})
rules.append({'idx': 2, 'from': 1, 'to': 2, 'guard': "(< x (- n t))"})
rules.append({'idx': 3, 'from': 2, 'to': 2, 'guard': "(< x (- n t))"})
rules.append({'idx': 4, 'from': 2, 'to': 3, 'guard': "(>= (+ x f) (- n t))"})
rules.append({'idx': 5, 'from': 3, 'to': 3, 'guard': "true"})
rules.append({'idx': 6, 'from': 0, 'to': 3, 'guard': "(>= (+ x f) (- n t))"})
rules.append({'idx': 7, 'from': 1, 'to': 3, 'guard': "(>= (+ x f) (- n t))"})

# parameters, resilience condition
params = ["n", "t", "f"]
active = "(- n f)"
rc = ["(> n 0)", "(>= t 0)", "(>= f 0)", "(>= t f)", "(> n (* 3 t))"]
phase = 1

# faults
faults = "byzantine"

# configuration/transition constraints
constraints = []
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': local, 'result': active})
constraints.append({'type': 'transition', 'sum': 'eq', 'object': range(len(rules)), 'result': active})


# properties
properties = []
properties.append({'name':"unforgeability", 'spec':'safety', 'initial':"(= x 0)", 'qf':'some', 'reachable':"(> acc 0)"})