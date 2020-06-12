# process local states
local = range(52)
# L states
L = {"x0" : [0, 16], "x1" : [1, 17], "k0" : [22], "k1" : [23], "m0" : [4, 5, 20, 21], "m1" : [3, 5, 19, 21],
     "y0" : [26, 42], "y1" : [27, 43], "ko0" : [48], "ko1" : [49], "mo0" : [30, 31, 46, 47], "mo1" : [29, 31, 45, 47]}
# initial states
initial = [0, 1, 16, 17, 26, 27, 42, 43]

#  m00: (<= x0 (+ x1 y1 to))
#  m01: (> (+ x0 y0) (+ x1 to))
#  m10: (<= x1 (+ x0 y0 to))
#  m11: (> (+ x1 y1) (+ x0 to))
#  ~d1: (<= m1 0)
#   d1: (> (+ m1 mo1) 0)
#  mv0: (<= m0 to)
# ~mv0: (> (+ m0 mo0) to)
#  mv1: (<= m1 to)
# ~mv1: (> (+ m1 mo1) to)

# rules
rules = []
rules.append({'idx': 0, 'from': 0, 'to': 2, 'guard': "(and (<= x0 (+ x1 y1 to)) (<= x1 (+ x0 y0 to)) )"})
rules.append({'idx': 1, 'from': 0, 'to': 3, 'guard': "(and (<= x0 (+ x1 y1 to)) (> (+ x1 y1) (+ x0 to)) )"})
rules.append({'idx': 2, 'from': 0, 'to': 4, 'guard': "(and (> (+ x0 y0) (+ x1 to)) (<= x1 (+ x0 y0 to)) )"})
rules.append({'idx': 3, 'from': 0, 'to': 5, 'guard': "(and (> (+ x0 y0) (+ x1 to)) (> (+ x1 y1) (+ x0 to)) )"})

rules.append({'idx': 4, 'from': 1, 'to': 2, 'guard': "(and (<= x0 (+ x1 y1 to)) (<= x1 (+ x0 y0 to)) )"})
rules.append({'idx': 5, 'from': 1, 'to': 3, 'guard': "(and (<= x0 (+ x1 y1 to)) (> (+ x1 y1) (+ x0 to)) )"})
rules.append({'idx': 6, 'from': 1, 'to': 4, 'guard': "(and (> (+ x0 y0) (+ x1 to)) (<= x1 (+ x0 y0 to)) )"})
rules.append({'idx': 7, 'from': 1, 'to': 5, 'guard': "(and (> (+ x0 y0) (+ x1 to)) (> (+ x1 y1) (+ x0 to)) )"})

rules.append({'idx': 8, 'from': 2, 'to': 6, 'guard': "(and (<= m1 0) (<= m0 to) )"})
rules.append({'idx': 9, 'from': 2, 'to': 7, 'guard': "(and (<= m1 0) (> (+ m0 mo0) to) )"})
rules.append({'idx': 10, 'from': 2, 'to': 8, 'guard': "(and (> (+ m1 mo1) 0) (<= m1 to) )"})
rules.append({'idx': 11, 'from': 2, 'to': 9, 'guard': "(and (> (+ m1 mo1) 0) (> (+ m1 mo1) to) )"})

rules.append({'idx': 12, 'from': 3, 'to': 6, 'guard': "(and (<= m1 0) (<= m0 to) )"})
rules.append({'idx': 13, 'from': 3, 'to': 7, 'guard': "(and (<= m1 0) (> (+ m0 mo0) to) )"})
rules.append({'idx': 14, 'from': 3, 'to': 8, 'guard': "(and (> (+ m1 mo1) 0) (<= m1 to) )"})
rules.append({'idx': 15, 'from': 3, 'to': 9, 'guard': "(and (> (+ m1 mo1) 0) (> (+ m1 mo1) to) )"})

rules.append({'idx': 16, 'from': 4, 'to': 6, 'guard': "(and (<= m1 0) (<= m0 to) )"})
rules.append({'idx': 17, 'from': 4, 'to': 7, 'guard': "(and (<= m1 0) (> (+ m0 mo0) to) )"})
rules.append({'idx': 18, 'from': 4, 'to': 8, 'guard': "(and (> (+ m1 mo1) 0) (<= m1 to) )"})
rules.append({'idx': 19, 'from': 4, 'to': 9, 'guard': "(and (> (+ m1 mo1) 0) (> (+ m1 mo1) to) )"})

rules.append({'idx': 20, 'from': 5, 'to': 6, 'guard': "(and (<= m1 0) (<= m0 to) )"})
rules.append({'idx': 21, 'from': 5, 'to': 7, 'guard': "(and (<= m1 0) (> (+ m0 mo0) to) )"})
rules.append({'idx': 22, 'from': 5, 'to': 8, 'guard': "(and (> (+ m1 mo1) 0) (<= m1 to) )"})
rules.append({'idx': 23, 'from': 5, 'to': 9, 'guard': "(and (> (+ m1 mo1) 0) (> (+ m1 mo1) to) )"})

rules.append({'idx': 24, 'from': 6, 'to': 10, 'guard': "(> (+ k0 ko0) 0)"})
rules.append({'idx': 25, 'from': 6, 'to': 11, 'guard': "(> (+ k1 ko1) 0)"})

rules.append({'idx': 26, 'from': 7, 'to': 12, 'guard': "true"})

rules.append({'idx': 27, 'from': 8, 'to': 13, 'guard': "(> (+ k0 ko0) 0)"})
rules.append({'idx': 28, 'from': 8, 'to': 14, 'guard': "(> (+ k1 ko1) 0)"})

rules.append({'idx': 29, 'from': 9, 'to': 15, 'guard': "true"})

# going back to the beginning of the round
rules.append({'idx': 30, 'from': 10, 'to': 0, 'guard': "true"})
rules.append({'idx': 31, 'from': 12, 'to': 0, 'guard': "true"})
rules.append({'idx': 32, 'from': 13, 'to': 0, 'guard': "true"})

rules.append({'idx': 33, 'from': 11, 'to': 1, 'guard': "true"})
rules.append({'idx': 34, 'from': 14, 'to': 1, 'guard': "true"})
rules.append({'idx': 35, 'from': 15, 'to': 1, 'guard': "true"})

rules.append({'idx': 36, 'from': 10, 'to': 16, 'guard': "true"})
rules.append({'idx': 37, 'from': 12, 'to': 16, 'guard': "true"})
rules.append({'idx': 38, 'from': 13, 'to': 16, 'guard': "true"})

rules.append({'idx': 39, 'from': 11, 'to': 17, 'guard': "true"})
rules.append({'idx': 40, 'from': 14, 'to': 17, 'guard': "true"})
rules.append({'idx': 41, 'from': 15, 'to': 17, 'guard': "true"})

# king transitions
rules.append({'idx': 42, 'from': 16, 'to': 18, 'guard': "(and (<= x0 (+ x1 y1 to)) (<= x1 (+ x0 y0 to)) )"})
rules.append({'idx': 43, 'from': 16, 'to': 19, 'guard': "(and (<= x0 (+ x1 y1 to)) (> (+ x1 y1) (+ x0 to)) )"})
rules.append({'idx': 44, 'from': 16, 'to': 20, 'guard': "(and (> (+ x0 y0) (+ x1 to)) (<= x1 (+ x0 y0 to)) )"})
rules.append({'idx': 45, 'from': 16, 'to': 21, 'guard': "(and (> (+ x0 y0) (+ x1 to)) (> (+ x1 y1) (+ x0 to)) )"})

rules.append({'idx': 46, 'from': 17, 'to': 18, 'guard': "(and (<= x0 (+ x1 y1 to)) (<= x1 (+ x0 y0 to)) )"})
rules.append({'idx': 47, 'from': 17, 'to': 19, 'guard': "(and (<= x0 (+ x1 y1 to)) (> (+ x1 y1) (+ x0 to)) )"})
rules.append({'idx': 48, 'from': 17, 'to': 20, 'guard': "(and (> (+ x0 y0) (+ x1 to)) (<= x1 (+ x0 y0 to)) )"})
rules.append({'idx': 49, 'from': 17, 'to': 21, 'guard': "(and (> (+ x0 y0) (+ x1 to)) (> (+ x1 y1) (+ x0 to)) )"})

rules.append({'idx': 50, 'from': 18, 'to': 22, 'guard': "(<= m1 0)"})
rules.append({'idx': 51, 'from': 18, 'to': 23, 'guard': "(> (+ m1 mo1) 0)"})

rules.append({'idx': 52, 'from': 19, 'to': 22, 'guard': "(<= m1 0)"})
rules.append({'idx': 53, 'from': 19, 'to': 23, 'guard': "(> (+ m1 mo1) 0)"})

rules.append({'idx': 54, 'from': 20, 'to': 22, 'guard': "(<= m1 0)"})
rules.append({'idx': 55, 'from': 20, 'to': 23, 'guard': "(> (+ m1 mo1) 0)"})

rules.append({'idx': 56, 'from': 21, 'to': 22, 'guard': "(<= m1 0)"})
rules.append({'idx': 57, 'from': 21, 'to': 23, 'guard': "(> (+ m1 mo1) 0)"})

rules.append({'idx': 58, 'from': 22, 'to': 24, 'guard': "true"})
rules.append({'idx': 59, 'from': 23, 'to': 25, 'guard': "true"})

# going back to the beginning of the round
rules.append({'idx': 60, 'from': 24, 'to': 0, 'guard': "true"})
rules.append({'idx': 61, 'from': 25, 'to': 1, 'guard': "true"})

# omission faulty processes transitions
rules.append({'idx': 62, 'from': 26, 'to': 28, 'guard': "(and (<= x0 (+ x1 y1 to)) (<= x1 (+ x0 y0 to)) )"})
rules.append({'idx': 63, 'from': 26, 'to': 29, 'guard': "(and (<= x0 (+ x1 y1 to)) (> (+ x1 y1) (+ x0 to)) )"})
rules.append({'idx': 64, 'from': 26, 'to': 30, 'guard': "(and (> (+ x0 y0) (+ x1 to)) (<= x1 (+ x0 y0 to)) )"})
rules.append({'idx': 65, 'from': 26, 'to': 31, 'guard': "(and (> (+ x0 y0) (+ x1 to)) (> (+ x1 y1) (+ x0 to)) )"})

rules.append({'idx': 66, 'from': 27, 'to': 28, 'guard': "(and (<= x0 (+ x1 y1 to)) (<= x1 (+ x0 y0 to)) )"})
rules.append({'idx': 67, 'from': 27, 'to': 29, 'guard': "(and (<= x0 (+ x1 y1 to)) (> (+ x1 y1) (+ x0 to)) )"})
rules.append({'idx': 68, 'from': 27, 'to': 30, 'guard': "(and (> (+ x0 y0) (+ x1 to)) (<= x1 (+ x0 y0 to)) )"})
rules.append({'idx': 69, 'from': 27, 'to': 31, 'guard': "(and (> (+ x0 y0) (+ x1 to)) (> (+ x1 y1) (+ x0 to)) )"})

rules.append({'idx': 70, 'from': 28, 'to': 32, 'guard': "(and (<= m1 0) (<= m0 to) )"})
rules.append({'idx': 71, 'from': 28, 'to': 33, 'guard': "(and (<= m1 0) (> (+ m0 mo0) to) )"})
rules.append({'idx': 72, 'from': 28, 'to': 34, 'guard': "(and (> (+ m1 mo1) 0) (<= m1 to) )"})
rules.append({'idx': 73, 'from': 28, 'to': 35, 'guard': "(and (> (+ m1 mo1) 0) (> (+ m1 mo1) to) )"})

rules.append({'idx': 74, 'from': 29, 'to': 32, 'guard': "(and (<= m1 0) (<= m0 to) )"})
rules.append({'idx': 75, 'from': 29, 'to': 33, 'guard': "(and (<= m1 0) (> (+ m0 mo0) to) )"})
rules.append({'idx': 76, 'from': 29, 'to': 34, 'guard': "(and (> (+ m1 mo1) 0) (<= m1 to) )"})
rules.append({'idx': 77, 'from': 29, 'to': 35, 'guard': "(and (> (+ m1 mo1) 0) (> (+ m1 mo1) to) )"})

rules.append({'idx': 78, 'from': 30, 'to': 32, 'guard': "(and (<= m1 0) (<= m0 to) )"})
rules.append({'idx': 79, 'from': 30, 'to': 33, 'guard': "(and (<= m1 0) (> (+ m0 mo0) to) )"})
rules.append({'idx': 80, 'from': 30, 'to': 34, 'guard': "(and (> (+ m1 mo1) 0) (<= m1 to) )"})
rules.append({'idx': 81, 'from': 30, 'to': 35, 'guard': "(and (> (+ m1 mo1) 0) (> (+ m1 mo1) to) )"})

rules.append({'idx': 82, 'from': 31, 'to': 32, 'guard': "(and (<= m1 0) (<= m0 to) )"})
rules.append({'idx': 83, 'from': 31, 'to': 33, 'guard': "(and (<= m1 0) (> (+ m0 mo0) to) )"})
rules.append({'idx': 84, 'from': 31, 'to': 34, 'guard': "(and (> (+ m1 mo1) 0) (<= m1 to) )"})
rules.append({'idx': 85, 'from': 31, 'to': 35, 'guard': "(and (> (+ m1 mo1) 0) (> (+ m1 mo1) to) )"})

rules.append({'idx': 86, 'from': 32, 'to': 36, 'guard': "(> (+ k0 ko0) 0)"})
rules.append({'idx': 87, 'from': 32, 'to': 37, 'guard': "(> (+ k1 ko1) 0)"})

rules.append({'idx': 88, 'from': 33, 'to': 38, 'guard': "true"})

rules.append({'idx': 89, 'from': 34, 'to': 39, 'guard': "(> (+ k0 ko0) 0)"})
rules.append({'idx': 90, 'from': 34, 'to': 40, 'guard': "(> (+ k1 ko1) 0)"})

rules.append({'idx': 91, 'from': 35, 'to': 41, 'guard': "true"})

# going back to the beginning of the round
rules.append({'idx': 92, 'from': 36, 'to': 26, 'guard': "true"})
rules.append({'idx': 93, 'from': 38, 'to': 26, 'guard': "true"})
rules.append({'idx': 94, 'from': 39, 'to': 26, 'guard': "true"})

rules.append({'idx': 95, 'from': 37, 'to': 27, 'guard': "true"})
rules.append({'idx': 96, 'from': 40, 'to': 27, 'guard': "true"})
rules.append({'idx': 97, 'from': 41, 'to': 27, 'guard': "true"})

rules.append({'idx': 98, 'from': 36, 'to': 42, 'guard': "true"})
rules.append({'idx': 99, 'from': 38, 'to': 42, 'guard': "true"})
rules.append({'idx': 100, 'from': 39, 'to': 42, 'guard': "true"})

rules.append({'idx': 101, 'from': 37, 'to': 43, 'guard': "true"})
rules.append({'idx': 102, 'from': 40, 'to': 43, 'guard': "true"})
rules.append({'idx': 103, 'from': 41, 'to': 43, 'guard': "true"})

# omission faulty king transitions
rules.append({'idx': 104, 'from': 42, 'to': 44, 'guard': "(and (<= x0 (+ x1 y1 to)) (<= x1 (+ x0 y0 to)) )"})
rules.append({'idx': 105, 'from': 42, 'to': 45, 'guard': "(and (<= x0 (+ x1 y1 to)) (> (+ x1 y1) (+ x0 to)) )"})
rules.append({'idx': 106, 'from': 42, 'to': 46, 'guard': "(and (> (+ x0 y0) (+ x1 to)) (<= x1 (+ x0 y0 to)) )"})
rules.append({'idx': 107, 'from': 42, 'to': 47, 'guard': "(and (> (+ x0 y0) (+ x1 to)) (> (+ x1 y1) (+ x0 to)) )"})

rules.append({'idx': 108, 'from': 43, 'to': 44, 'guard': "(and (<= x0 (+ x1 y1 to)) (<= x1 (+ x0 y0 to)) )"})
rules.append({'idx': 109, 'from': 43, 'to': 45, 'guard': "(and (<= x0 (+ x1 y1 to)) (> (+ x1 y1) (+ x0 to)) )"})
rules.append({'idx': 110, 'from': 43, 'to': 46, 'guard': "(and (> (+ x0 y0) (+ x1 to)) (<= x1 (+ x0 y0 to)) )"})
rules.append({'idx': 111, 'from': 43, 'to': 47, 'guard': "(and (> (+ x0 y0) (+ x1 to)) (> (+ x1 y1) (+ x0 to)) )"})

rules.append({'idx': 112, 'from': 44, 'to': 48, 'guard': "(<= m1 0)"})
rules.append({'idx': 113, 'from': 44, 'to': 49, 'guard': "(> (+ m1 mo1) 0)"})

rules.append({'idx': 114, 'from': 45, 'to': 48, 'guard': "(<= m1 0)"})
rules.append({'idx': 115, 'from': 45, 'to': 49, 'guard': "(> (+ m1 mo1) 0)"})

rules.append({'idx': 116, 'from': 46, 'to': 48, 'guard': "(<= m1 0)"})
rules.append({'idx': 117, 'from': 46, 'to': 49, 'guard': "(> (+ m1 mo1) 0)"})

rules.append({'idx': 118, 'from': 47, 'to': 48, 'guard': "(<= m1 0)"})
rules.append({'idx': 119, 'from': 47, 'to': 49, 'guard': "(> (+ m1 mo1) 0)"})

rules.append({'idx': 120, 'from': 48, 'to': 50, 'guard': "true"})
rules.append({'idx': 121, 'from': 49, 'to': 51, 'guard': "true"})

# going back to the beginning of the round
rules.append({'idx': 122, 'from': 50, 'to': 26, 'guard': "true"})
rules.append({'idx': 123, 'from': 51, 'to': 27, 'guard': "true"})

# additional rules that introduce non-determinism when the king is send-omission faulty
rules.append({'idx': 124, 'from': 6, 'to': 10, 'guard': "(> (+ ko0 ko1) 0)"})
rules.append({'idx': 125, 'from': 8, 'to': 14, 'guard': "(> (+ ko0 ko1) 0)"})

rules.append({'idx': 126, 'from': 32, 'to': 36, 'guard': "(> (+ ko0 ko1) 0)"})
rules.append({'idx': 127, 'from': 34, 'to': 40, 'guard': "(> (+ ko0 ko1) 0)"})

# parameters, resilience condition
params = ["n", "to", "fo"]
active = "n"
rc = ["(> n 0)", "(> to 0)", "(> fo 0)", "(>= to fo)", "(> n (* 2 to))"]

# faults
faults = "omission"
faulty = range(26, 52)
max_faulty = "fo"

omit_king = list(range(42, 52))
king = list(range(16, 26)) + omit_king
phase = 4

# configuration/transition constraints
constraints = []
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': local, 'result': active})
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': faulty, 'result': max_faulty})
constraints.append({'type': 'configuration', 'sum': 'eq', 'object': king, 'result': 1})
constraints.append({'type': 'transition', 'sum': 'eq', 'object': range(len(rules)), 'result': active})
constraints.append({'type': 'round_config', 'sum': 'eq', 'object': omit_king, 'result': 0})

properties = []
properties.append({'name':'validity0', 'spec':'safety', 'initial':'(= (+ x0 y0) n)', 'qf':'some', 'reachable':'(not (= (+ x1 y1) 0))'})
properties.append({'name':'validity1', 'spec':'safety', 'initial':'(= (+ x1 y1) n)', 'qf':'some', 'reachable':'(not (= (+ x0 y0) 0))'})
properties.append({'name':'agreement', 'spec':'safety', 'initial':'true', 'qf':'last', 'reachable':'(and (not (= (+ x0 y0) 0)) (not (= (+ x1 y1) 0)))'})
