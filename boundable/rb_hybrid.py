# process local states
local = range(8)
# L states
L = {"x" : [1, 2, 3], "y" : [5, 6, 7], "acc" : [3, 7]}
# initial states
initial = [0, 1, 4, 5]

# rules
rules = []
rules.append({'idx': 0, 'from': 0, 'to': 0, 'guard': "(< x (- n (* 2 tb) (* 2 to)))"})
rules.append({'idx': 1, 'from': 0, 'to': 2, 'guard': "(>= (+ x y fb) (- n (* 2 tb) (* 2 to)))"}) 
rules.append({'idx': 2, 'from': 1, 'to': 2, 'guard': "(< x (- n tb to))"})
rules.append({'idx': 3, 'from': 2, 'to': 2, 'guard': "(< x (- n tb to))"})
rules.append({'idx': 4, 'from': 2, 'to': 3, 'guard': "(>= (+ x y fb) (- n tb to))"})
rules.append({'idx': 5, 'from': 3, 'to': 3, 'guard': "true"})
rules.append({'idx': 6, 'from': 0, 'to': 3, 'guard': "(>= (+ x y fb) (- n tb to))"})
rules.append({'idx': 7, 'from': 1, 'to': 3, 'guard': "(>= (+ x y fb) (- n tb to))"})

rules.append({'idx': 8, 'from': 4, 'to': 4, 'guard': "(< x (- n (* 2 tb) (* 2 to)))"})
rules.append({'idx': 9, 'from': 4, 'to': 6, 'guard': "(>= (+ x y fb) (- n (* 2 tb) (* 2 to)))"})
rules.append({'idx': 10, 'from': 5, 'to': 6, 'guard': "(< x (- n tb to))"})
rules.append({'idx': 11, 'from': 6, 'to': 6, 'guard': "(< x (- n tb to))"})
rules.append({'idx': 12, 'from': 6, 'to': 7, 'guard': "(>= (+ x y fb) (- n tb to))"})
rules.append({'idx': 13, 'from': 7, 'to': 7, 'guard': "true"})
rules.append({'idx': 14, 'from': 4, 'to': 7, 'guard': "(>= (+ x y fb) (- n tb to))"})
rules.append({'idx': 15, 'from': 5, 'to': 7, 'guard': "(>= (+ x y fb) (- n tb to))"})

# parameters, resilience condition
params = ["n", "tb", "to", "fb", "fo"]
active = "(- n fb)"
rc = ["(> n 0)", "(>= tb 0)", "(>= to 0)", "(>= fb 0)", "(>= fo 0)", "(>= tb fb)", "(>= to fo)", "(> n (+ (* 2 to) (* 3 tb)))"]

# faults
faults = "hybrid"
faulty = [4, 5, 6, 7]
max_faulty = "fo"
phase = 1

# configuration/transition constraints
constraints = []
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': local, 'result': active})
constraints.append({'type': 'configuration', 'sum': 'le', 'object': faulty, 'result': max_faulty})
constraints.append({'type': 'transition', 'sum': 'eq', 'object': range(len(rules)), 'result': active})

# properties
properties = []
properties.append({'name':"unforgeability", 'spec':'safety', 'initial':"(= (+ x y) 0)", 'qf':'some', 'reachable':"(> acc 0)"})
# properties.append({'name':"correctness", 'spec':'liveness', 'initial':"(= (+ x y) (- n fb))", 'qf':'all', 'reachable':"(< acc (- n fb))"})
