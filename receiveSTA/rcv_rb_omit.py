# process local states
local = range(8)
# L states
L = {"x" : [1, 2, 3], "y" : [5, 6, 7], "acc" : [3, 7]}
# receive variables 
rcv_vars = ["nr"]
# initial states
initial = [0, 1, 4, 5]

# rules
rules = []
rules.append({'idx': 0, 'from': 0, 'to': 0, 'guard': "(< nr (- n (* 2 t)))"}) 
rules.append({'idx': 1, 'from': 0, 'to': 2, 'guard': "(>= nr (- n (* 2 t)))"}) 
rules.append({'idx': 2, 'from': 1, 'to': 2, 'guard': "(< nr (- n t))"})
rules.append({'idx': 3, 'from': 2, 'to': 2, 'guard': "(< nr (- n t))"})
rules.append({'idx': 4, 'from': 2, 'to': 3, 'guard': "(>= nr (- n t))"})
rules.append({'idx': 5, 'from': 3, 'to': 3, 'guard': "true"})
rules.append({'idx': 6, 'from': 0, 'to': 3, 'guard': "(>= nr (- n t))"})
rules.append({'idx': 7, 'from': 1, 'to': 3, 'guard': "(>= nr (- n t))"})

rules.append({'idx': 8, 'from': 4, 'to': 4, 'guard': "(< nr (- n (* 2 t)))"}) 
rules.append({'idx': 9, 'from': 4, 'to': 6, 'guard': "(>= nr (- n (* 2 t)))"}) 
rules.append({'idx': 10, 'from': 5, 'to': 6, 'guard': "(< nr (- n t))"})
rules.append({'idx': 11, 'from': 6, 'to': 6, 'guard': "(< nr (- n t))"})
rules.append({'idx': 12, 'from': 6, 'to': 7, 'guard': "(>= nr (- n t))"})
rules.append({'idx': 13, 'from': 7, 'to': 7, 'guard': "true"})
rules.append({'idx': 14, 'from': 4, 'to': 7, 'guard': "(>= nr (- n t))"})
rules.append({'idx': 15, 'from': 5, 'to': 7, 'guard': "(>= nr (- n t))"})
 
# parameters, resilience condition
params = ["n", "t", "f"]
active = "n"
rc = ["(> n 0)", "(>= t 0)", "(>= t f)", "(> n (* 2 t))"]

# faults
faults = "omission"
faulty = [4, 5, 6, 7]
max_faulty = "f"
phase = 1

# configuration/transition constraints
constraints = []
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': local, 'result': active})
constraints.append({'type': 'configuration', 'sum': 'le', 'object': faulty, 'result': max_faulty})
constraints.append({'type': 'transition', 'sum': 'eq', 'object': range(len(rules)), 'result': active})

# receive environment constraints
environment = []
environment.append('(>= nr x)')
environment.append('(<= nr (+ x y))')

# properties
properties = []
properties.append({'name':"unforgeability", 'spec':'safety', 'initial':"(= (+ x y) 0)", 'qf':'some', 'reachable':"(> acc 0)"})