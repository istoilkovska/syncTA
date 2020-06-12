# process local states
local = range(24)
# L states
L = {"x0" : [0, 12], "x1" : [1, 13], "q0" : [14], "q1" : [15], "qf" : [20]}
# initial states
initial = [0, 1, 12, 13, 18, 19]

# rules
rules = []
rules.append({'idx': 0, 'from': 0, 'to': 2, 'guard': "(and (<= x1 (* 2 t)) (< x0 (- n t)))"})
rules.append({'idx': 1, 'from': 0, 'to': 3, 'guard': "(and (<= x1 (* 2 t)) (>= x0 (- (- n t) f)))"})
rules.append({'idx': 2, 'from': 0, 'to': 4, 'guard': "(and (> x1 (- (* 2 t) f)) (< x1 (- n t)))"})
rules.append({'idx': 3, 'from': 0, 'to': 5, 'guard': "(and (> x1 (- (* 2 t) f)) (>= x1 (- (- n t) f)))"})

rules.append({'idx': 4, 'from': 1, 'to': 2, 'guard': "(and (<= x1 (* 2 t)) (< x0 (- n t)))"})
rules.append({'idx': 5, 'from': 1, 'to': 3, 'guard': "(and (<= x1 (* 2 t)) (>= x0 (- (- n t) f)))"})
rules.append({'idx': 6, 'from': 1, 'to': 4, 'guard': "(and (> x1 (- (* 2 t) f)) (< x1 (- n t)))"})
rules.append({'idx': 7, 'from': 1, 'to': 5, 'guard': "(and (> x1 (- (* 2 t) f)) (>= x1 (- (- n t) f)))"})

rules.append({'idx': 8, 'from': 2, 'to': 6, 'guard': "(> (+ q0 qf) 0)"})
rules.append({'idx': 9, 'from': 2, 'to': 7, 'guard': "(> (+ q1 qf) 0)"})

rules.append({'idx': 10, 'from': 3, 'to': 8, 'guard': "true"})

rules.append({'idx': 11, 'from': 4, 'to': 9, 'guard': "(> (+ q0 qf) 0)"})
rules.append({'idx': 12, 'from': 4, 'to': 10, 'guard': "(> (+ q1 qf) 0)"})

rules.append({'idx': 13, 'from': 5, 'to': 11, 'guard': "true"})

# going back to the beginning of the round
rules.append({'idx': 14, 'from': 6, 'to': 0, 'guard': "true"})
rules.append({'idx': 15, 'from': 8, 'to': 0, 'guard': "true"})
rules.append({'idx': 16, 'from': 9, 'to': 0, 'guard': "true"})

rules.append({'idx': 17, 'from': 7, 'to': 1, 'guard': "true"})
rules.append({'idx': 18, 'from': 10, 'to': 1, 'guard': "true"})
rules.append({'idx': 19, 'from': 11, 'to': 1, 'guard': "true"})

rules.append({'idx': 20, 'from': 6, 'to': 12, 'guard': "true"})
rules.append({'idx': 21, 'from': 8, 'to': 12, 'guard': "true"})
rules.append({'idx': 22, 'from': 9, 'to': 12, 'guard': "true"})

rules.append({'idx': 23, 'from': 7, 'to': 13, 'guard': "true"})
rules.append({'idx': 24, 'from': 10, 'to': 13, 'guard': "true"})
rules.append({'idx': 25, 'from': 11, 'to': 13, 'guard': "true"})

# queen transitions
rules.append({'idx': 26, 'from': 12, 'to': 14, 'guard': "(<= x1 (* 2 t))"})
rules.append({'idx': 27, 'from': 12, 'to': 15, 'guard': "(> x1 (- (* 2 t) f))"})

rules.append({'idx': 28, 'from': 13, 'to': 14, 'guard': "(<= x1 (* 2 t))"})
rules.append({'idx': 29, 'from': 13, 'to': 15, 'guard': "(> x1 (- (* 2 t) f))"})

rules.append({'idx': 30, 'from': 14, 'to': 16, 'guard': "true"})
rules.append({'idx': 31, 'from': 15, 'to': 17, 'guard': "true"})

# going back to the beginning of the round
rules.append({'idx': 32, 'from': 16, 'to': 0, 'guard': "true"})
rules.append({'idx': 33, 'from': 17, 'to': 1, 'guard': "true"})

# faulty queen transitions
rules.append({'idx': 34, 'from': 18, 'to': 20, 'guard': "true"})
rules.append({'idx': 35, 'from': 20, 'to': 22, 'guard': "true"})
rules.append({'idx': 36, 'from': 22, 'to': 18, 'guard': "true"})
rules.append({'idx': 37, 'from': 22, 'to': 19, 'guard': "true"})

rules.append({'idx': 38, 'from': 19, 'to': 21, 'guard': "true"})
rules.append({'idx': 39, 'from': 21, 'to': 23, 'guard': "true"})
rules.append({'idx': 40, 'from': 23, 'to': 18, 'guard': "true"})
rules.append({'idx': 41, 'from': 23, 'to': 19, 'guard': "true"})

# parameters, resilience condition
params = ["n", "t", "f"]
active = "(- n (- f 1))"
rc = ["(> n 0)", "(> t 0)", "(> f 0)", "(>= t f)", "(>= n (* 4 t))"]
# RESILIENCE CONDITION INTRODUCING MORE FAULTS: n >= 4t rather than n > 4t

# faults
faults = "byzantine"
faulty = [18, 19, 20, 21, 22, 23]
max_faulty = "1"

queen = [12, 13, 14, 15, 16, 17, 18, 20, 22]
faulty_queen = [18, 20, 22]
phase = 3

# configuration/transition constraints
constraints = []
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': local, 'result': active})
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': faulty, 'result': max_faulty})
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': queen, 'result': "1"})
constraints.append({'type': 'transition', 'sum': 'eq', 'object': range(len(rules)), 'result': active})
constraints.append({'type': 'round_config', 'sum': 'eq', 'object': faulty_queen, 'result': 0})

properties = []
properties.append({'name':'validity0', 'spec':'safety', 'initial':'(= x0 (- n f))', 'qf':'some', 'reachable':'(not (= x1 0))'})
properties.append({'name':'validity1', 'spec':'safety', 'initial':'(= x1 (- n f))', 'qf':'some', 'reachable':'(not (= x0 0))'})
properties.append({'name':'agreement', 'spec':'safety', 'initial':'true', 'qf':'last', 'reachable':'(and (not (= x0 0)) (not (= x1 0)))'})
