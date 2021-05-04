# process local states
local = range(42)
# L states
L = {"x0" : [0, 12], "x1" : [1, 13], "q0" : [14], "q1" : [15], "qb" : [20],
     "y0" : [24, 36], "y1" : [25, 37], "qo0" : [38], "qo1" : [39]
    }
initial = [0, 1, 12, 13, 18, 19, 24, 25, 36, 37]

 
# v0 : (<= x1 (+ x0 y0 fb))
# v1 : (> (+ x1 y1) (- x0 fb))
# c0 : (<= x0 (+ x1 y1 (* 2 tb) to fb))
# ~c0 : (> (+ x0 y0) (- (+ x1 (* 2 tb) to) fb))
# c1 : (<= x1 (+ x0 y0 (* 2 tb) to fb))
# ~c1 : (> (+ x1 y1) (- (+ x0 (* 2 tb) to) fb))

rules = []
rules.append({'idx': 0, 'from': 0, 'to': 2, 'guard': "(and (<= x1 (+ x0 y0 fb)) (<= x0 (+ x1 y1 (* 2 tb) to fb)) )"})
rules.append({'idx': 1, 'from': 0, 'to': 3, 'guard': "(and (<= x1 (+ x0 y0 fb)) (> (+ x0 y0) (- (+ x1 (* 2 tb) to) fb)) )"})
rules.append({'idx': 2, 'from': 0, 'to': 4, 'guard': "(and (> (+ x1 y1) (- x0 fb)) (<= x1 (+ x0 y0 (* 2 tb) to fb)) )"})
rules.append({'idx': 3, 'from': 0, 'to': 5, 'guard': "(and (> (+ x1 y1) (- x0 fb)) (> (+ x1 y1) (- (+ x0 (* 2 tb) to) fb)) )"})

rules.append({'idx': 4, 'from': 1, 'to': 2, 'guard': "(and (<= x1 (+ x0 y0 fb)) (<= x0 (+ x1 y1 (* 2 tb) to fb)) )"})
rules.append({'idx': 5, 'from': 1, 'to': 3, 'guard': "(and (<= x1 (+ x0 y0 fb)) (> (+ x0 y0) (- (+ x1 (* 2 tb) to) fb)) )"})
rules.append({'idx': 6, 'from': 1, 'to': 4, 'guard': "(and (> (+ x1 y1) (- x0 fb)) (<= x1 (+ x0 y0 (* 2 tb) to fb)) )"})
rules.append({'idx': 7, 'from': 1, 'to': 5, 'guard': "(and (> (+ x1 y1) (- x0 fb)) (> (+ x1 y1) (- (+ x0 (* 2 tb) to) fb)) )"})

rules.append({'idx': 8, 'from': 2, 'to': 6, 'guard': "(> (+ q0 qb qo0) 0)"})
rules.append({'idx': 9, 'from': 2, 'to': 7, 'guard': "(> (+ q1 qb qo1) 0)"})

rules.append({'idx': 10, 'from': 3, 'to': 8, 'guard': "true"})

rules.append({'idx': 11, 'from': 4, 'to': 9, 'guard': "(> (+ q0 qb qo0) 0)"})
rules.append({'idx': 12, 'from': 4, 'to': 10, 'guard': "(> (+ q1 qb qo1) 0)"})

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
rules.append({'idx': 26, 'from': 12, 'to': 14, 'guard': "(<= x1 (+ x0 y0 fb))"})
rules.append({'idx': 27, 'from': 12, 'to': 15, 'guard': "(> (+ x1 y1) (- x0 fb))"})

rules.append({'idx': 28, 'from': 13, 'to': 14, 'guard': "(<= x1 (+ x0 y0 fb))"})
rules.append({'idx': 29, 'from': 13, 'to': 15, 'guard': "(> (+ x1 y1) (- x0 fb))"})

rules.append({'idx': 30, 'from': 14, 'to': 16, 'guard': "true"})
rules.append({'idx': 31, 'from': 15, 'to': 17, 'guard': "true"})

# going back to the beginning of the round
rules.append({'idx': 32, 'from': 16, 'to': 0, 'guard': "true"})
rules.append({'idx': 33, 'from': 17, 'to': 1, 'guard': "true"})

# byzantine faulty queen transitions
rules.append({'idx': 34, 'from': 18, 'to': 20, 'guard': "true"})
rules.append({'idx': 35, 'from': 20, 'to': 22, 'guard': "true"})
rules.append({'idx': 36, 'from': 22, 'to': 18, 'guard': "true"})
rules.append({'idx': 37, 'from': 22, 'to': 19, 'guard': "true"})

rules.append({'idx': 38, 'from': 19, 'to': 21, 'guard': "true"})
rules.append({'idx': 39, 'from': 21, 'to': 23, 'guard': "true"})
rules.append({'idx': 40, 'from': 23, 'to': 18, 'guard': "true"})
rules.append({'idx': 41, 'from': 23, 'to': 19, 'guard': "true"})

# omission faulty processes transitions
rules.append({'idx': 42, 'from': 24, 'to': 26, 'guard': "(and (<= x1 (+ x0 y0 fb)) (<= x0 (+ x1 y1 (* 2 tb) to fb)) )"})
rules.append({'idx': 43, 'from': 24, 'to': 27, 'guard': "(and (<= x1 (+ x0 y0 fb)) (> (+ x0 y0) (- (+ x1 (* 2 tb) to) fb)) )"})
rules.append({'idx': 44, 'from': 24, 'to': 28, 'guard': "(and (> (+ x1 y1) (- x0 fb)) (<= x1 (+ x0 y0 (* 2 tb) to fb)) )"})
rules.append({'idx': 45, 'from': 24, 'to': 29, 'guard': "(and (> (+ x1 y1) (- x0 fb)) (> (+ x1 y1) (- (+ x0 (* 2 tb) to) fb)) )"})

rules.append({'idx': 46, 'from': 25, 'to': 26, 'guard': "(and (<= x1 (+ x0 y0 fb)) (<= x0 (+ x1 y1 (* 2 tb) to fb)) )"})
rules.append({'idx': 47, 'from': 25, 'to': 27, 'guard': "(and (<= x1 (+ x0 y0 fb)) (> (+ x0 y0) (- (+ x1 (* 2 tb) to) fb)) )"})
rules.append({'idx': 48, 'from': 25, 'to': 28, 'guard': "(and (> (+ x1 y1) (- x0 fb)) (<= x1 (+ x0 y0 (* 2 tb) to fb)) )"})
rules.append({'idx': 49, 'from': 25, 'to': 29, 'guard': "(and (> (+ x1 y1) (- x0 fb)) (> (+ x1 y1) (- (+ x0 (* 2 tb) to) fb)) )"})

rules.append({'idx': 50, 'from': 26, 'to': 30, 'guard': "(> (+ q0 qb qo0) 0)"})
rules.append({'idx': 51, 'from': 26, 'to': 31, 'guard': "(> (+ q1 qb qo1) 0)"})

rules.append({'idx': 52, 'from': 27, 'to': 32, 'guard': "true"})

rules.append({'idx': 53, 'from': 28, 'to': 33, 'guard': "(> (+ q0 qb qo0) 0)"})
rules.append({'idx': 54, 'from': 28, 'to': 34, 'guard': "(> (+ q1 qb qo1) 0)"})

rules.append({'idx': 55, 'from': 29, 'to': 35, 'guard': "true"})

# going back to the beginning of the round
rules.append({'idx': 56, 'from': 30, 'to': 24, 'guard': "true"})
rules.append({'idx': 57, 'from': 32, 'to': 24, 'guard': "true"})
rules.append({'idx': 58, 'from': 33, 'to': 24, 'guard': "true"})

rules.append({'idx': 59, 'from': 31, 'to': 25, 'guard': "true"})
rules.append({'idx': 60, 'from': 34, 'to': 25, 'guard': "true"})
rules.append({'idx': 61, 'from': 35, 'to': 25, 'guard': "true"})

rules.append({'idx': 62, 'from': 30, 'to': 36, 'guard': "true"})
rules.append({'idx': 63, 'from': 32, 'to': 36, 'guard': "true"})
rules.append({'idx': 64, 'from': 33, 'to': 36, 'guard': "true"})

rules.append({'idx': 65, 'from': 31, 'to': 37, 'guard': "true"})
rules.append({'idx': 66, 'from': 34, 'to': 37, 'guard': "true"})
rules.append({'idx': 67, 'from': 35, 'to': 37, 'guard': "true"})


# omission faulty queen transitions
rules.append({'idx': 68, 'from': 36, 'to': 38, 'guard': "(<= x1 (+ x0 y0 fb))"})
rules.append({'idx': 69, 'from': 36, 'to': 39, 'guard': "(> (+ x1 y1) (- x0 fb))"})

rules.append({'idx': 70, 'from': 37, 'to': 38, 'guard': "(<= x1 (+ x0 y0 fb))"})
rules.append({'idx': 71, 'from': 37, 'to': 39, 'guard': "(> (+ x1 y1) (- x0 fb))"})

rules.append({'idx': 72, 'from': 38, 'to': 40, 'guard': "true"})
rules.append({'idx': 73, 'from': 39, 'to': 41, 'guard': "true"})

# going back to the beginning of the round
rules.append({'idx': 74, 'from': 40, 'to': 24, 'guard': "true"})
rules.append({'idx': 75, 'from': 41, 'to': 25, 'guard': "true"})

# additional rules that introduce non-determinism when the queen is send-omission faulty
rules.append({'idx': 76, 'from': 2, 'to': 6, 'guard': "(> (+ qo0 qo1 qb) 0)"})
rules.append({'idx': 77, 'from': 4, 'to': 9, 'guard': "(> (+ qo0 qo1 qb) 0)"})

rules.append({'idx': 78, 'from': 26, 'to': 30, 'guard': "(> (+ qo0 qo1 qb) 0)"})
rules.append({'idx': 79, 'from': 28, 'to': 33, 'guard': "(> (+ qo0 qo1 qb) 0)"})

# parameters, resilience condition
params = ["n", "tb", "to", "fb", "fo"]
active = "(- n (- fb 1))"
rc = ["(> n 0)", "(>= tb 0)", "(>= to 0)", "(>= fb 0)", "(>= fo 0)", "(>= tb fb)", "(>= to fo)", "(> n (+ (* 2 to) (* 4 tb)))"]

# faults
faults = "hybrid"
byzantine = list(range(18, 24))
max_byzantine = 1
omission = list(range(24, 42))
max_omission = "fo"

byz_queen = [18, 20, 22]
omit_queen = list(range(36, 42))
queen = list(range(12, 18)) + byz_queen + omit_queen
phase = 3

# configuration/transition constraints
constraints = []
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': local, 'result': active})
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': byzantine, 'result': max_byzantine})
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': omission, 'result': max_omission})
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': queen, 'result': 1})
constraints.append({'type': 'transition', 'sum': 'eq', 'object': range(len(rules)), 'result': active})
constraints.append({'type': 'round_config', 'sum': 'eq', 'object': byz_queen + omit_queen, 'result': 0})

properties = []
properties.append({'name':'validity0', 'spec':'safety', 'initial':'(= (+ x0 y0) (- n fb))', 'qf':'some', 'reachable':'(not (= (+ x1 y1) 0))'})
properties.append({'name':'validity1', 'spec':'safety', 'initial':'(= (+ x1 y1) (- n fb))', 'qf':'some', 'reachable':'(not (= (+ x0 y0) 0))'})
properties.append({'name':'agreement', 'spec':'safety', 'initial':'true', 'qf':'last', 'reachable':'(and (not (= (+ x0 y0) 0)) (not (= (+ x1 y1) 0)))'})
