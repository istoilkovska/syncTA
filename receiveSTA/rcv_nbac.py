# process local states
local = range(11)
# L states
L = {"n0" : [0], "nf0" : [2], "n1" : [1], "nf1" : [3], 
     "x0" : [4, 6], "x1" : [5, 6], "cr0" : [7, 9], "cr1" : [8, 9], 
     "v0" : [4, 7], "v1" : [5, 8], "d0" : [4, 6], "d1" : [5]}
# receive variables 
rcv_vars = ["nrY", "nrN", "nr0", "nr1"]
# initial states
initial = [0, 1, 2, 3]

# rules
rules = []
rules.append({'idx': 0, 'from': 0, 'to': 5, 'guard': "(and (>= (+ nrY nrN) n) (= nrN 0))"})
rules.append({'idx': 1, 'from': 1, 'to': 5, 'guard': "(and (>= (+ nrY nrN) n) (= nrN 0))"})
rules.append({'idx': 2, 'from': 0, 'to': 8, 'guard': "(and (>= (+ nrY nrN) n) (= nrN 0))"})
rules.append({'idx': 3, 'from': 1, 'to': 8, 'guard': "(and (>= (+ nrY nrN) n) (= nrN 0))"})

rules.append({'idx': 4, 'from': 0, 'to': 4, 'guard': "(or (< (+ nrY nrN) n) (> nrN 0))"})
rules.append({'idx': 5, 'from': 1, 'to': 4, 'guard': "(or (< (+ nrY nrN) n) (> nrN 0))"})
rules.append({'idx': 6, 'from': 0, 'to': 7, 'guard': "(or (< (+ nrY nrN) n) (> nrN 0))"})
rules.append({'idx': 7, 'from': 1, 'to': 7, 'guard': "(or (< (+ nrY nrN) n) (> nrN 0))"})

# rules.append({'idx': 0, 'from': 0, 'to': 5, 'guard': "(and (= nrY n)"})
# rules.append({'idx': 1, 'from': 1, 'to': 5, 'guard': "(= nrY n)"})
# rules.append({'idx': 2, 'from': 0, 'to': 8, 'guard': "(= nrY n)"})
# rules.append({'idx': 3, 'from': 1, 'to': 8, 'guard': "(= nrY n)"})

# rules.append({'idx': 24, 'from': 0, 'to': 4, 'guard': "(and (< nrY n) (= nrN 0))"})
# rules.append({'idx': 25, 'from': 1, 'to': 4, 'guard': "(and (< nrY n) (= nrN 0))"})
# rules.append({'idx': 26, 'from': 0, 'to': 7, 'guard': "(and (< nrY n) (= nrN 0))"})
# rules.append({'idx': 27, 'from': 1, 'to': 7, 'guard': "(and (< nrY n) (= nrN 0))"})

# rules.append({'idx': 4, 'from': 0, 'to': 4, 'guard': "(> nrN 0)"})
# rules.append({'idx': 5, 'from': 1, 'to': 4, 'guard': "(> nrN 0)"})
# rules.append({'idx': 6, 'from': 0, 'to': 7, 'guard': "(> nrN 0)"})
# rules.append({'idx': 7, 'from': 1, 'to': 7, 'guard': "(> nrN 0)"})


rules.append({'idx': 8, 'from': 2, 'to': 10, 'guard': "true"})
rules.append({'idx': 9, 'from': 3, 'to': 10, 'guard': "true"})

rules.append({'idx': 10, 'from': 4, 'to': 4, 'guard': "(< nr1 1)"})
rules.append({'idx': 11, 'from': 4, 'to': 6, 'guard': "(>= nr1 1)"})
rules.append({'idx': 12, 'from': 6, 'to': 6, 'guard': "true"})
rules.append({'idx': 13, 'from': 5, 'to': 6, 'guard': "(>= nr0 1)"})
rules.append({'idx': 14, 'from': 5, 'to': 5, 'guard': "(< nr0 1)"})
rules.append({'idx': 15, 'from': 4, 'to': 7, 'guard': "(< nr1 1)"})
rules.append({'idx': 16, 'from': 4, 'to': 9, 'guard': "(>= nr1 1)"})
rules.append({'idx': 17, 'from': 6, 'to': 9, 'guard': "true"})
rules.append({'idx': 18, 'from': 5, 'to': 9, 'guard': "(>= nr0 1)"})
rules.append({'idx': 19, 'from': 5, 'to': 8, 'guard': "(< nr0 1)"})
rules.append({'idx': 20, 'from': 7, 'to': 10, 'guard': "true"})
rules.append({'idx': 21, 'from': 9, 'to': 10, 'guard': "true"})
rules.append({'idx': 22, 'from': 8, 'to': 10, 'guard': "true"})
rules.append({'idx': 23, 'from': 10, 'to': 10, 'guard': "true"})

# parameters, resilience condition
params = ["n", "t", "f"]
active = "n"
rc = ["(> n 0)", "(>= t 0)", "(>= t f)", "(> n t)"]

# faults
faults = "crash"
faulty = [2, 3, 7, 8, 9, 10]
crashed = [2, 3, 7, 8, 9]
max_faulty = "f"
phase = 1


# configuration/transition constraints
constraints = []
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': local, 'result': active})
constraints.append({'type': 'configuration', 'sum': 'le', 'object': faulty, 'result': max_faulty})
constraints.append({'type': 'transition', 'sum': 'eq', 'object': range(len(rules)), 'result': active})
constraints.append({'type': 'round_config', 'sum': 'eq', 'object': crashed, 'result': 0})

# receive environment constraints
environment = []
environment.append('(>= nrY n1)')
environment.append('(<= nrY (+ n1 nf1))')
environment.append('(>= nrN n0)')
environment.append('(<= nrN (+ n0 nf0))')
environment.append('(>= nr0 x0)')
environment.append('(<= nr0 (+ x0 cr0))')
environment.append('(>= nr1 x1)')
environment.append('(<= nr1 (+ x1 cr1))')
environment.append('(= (+ n0 n1 nf0 nf1) n)')

# properties
properties = []
properties.append({'name':'obligation', 'spec':'safety', 'initial':'(= n1 n)', 'qf':'last', 'reachable':'(> d0 0)'})
properties.append({'name':'justification', 'spec':'safety', 'initial':'(= (+ n1 nf1) n)', 'qf':'last', 'reachable':'(> d0 0)'})
properties.append({'name':'agreement', 'spec':'safety', 'initial':'true', 'qf':'last', 'reachable':'(and (> d0 0) (> d1 0))'})
