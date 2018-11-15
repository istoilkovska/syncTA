def new_constant(const_name):
    return "(declare-const " + const_name + " Int)\n"

def parameters(params):
    result = ""
    for p in params:  
        result += new_constant(p)
    return result

def declare_constants(start, idx1, idx2, symbol):
    result = ""
    for i in range(start, idx1):
        for j in range(idx2):
            const_name = symbol + str(i) + "_" + str(j)
            result += new_constant(const_name)
    return result

def list_conjunction(l):
    result = "(and"
    for item in l:
        result += " " + item
    result += ")\n"
    return result

def sum_counters_eq(sum_cnt, num):
    return "(= (+ " + sum_cnt + ") " + str(num) + ")\n"

def sum_counters_le(sum_cnt, num):
    return "(<= (+ " + sum_cnt + ") " + str(num) + ")\n"

def non_negative(start, idx1, idx2, symbol):
    result = ""
    for i in range(start, idx1):
        for j in range(idx2):
            const_name = symbol + str(i) + "_" + str(j)
            result += "(>= " + const_name + " 0)\n"
    return result

def add_constraint(start, idx, symbol, relation, constrained_obj, value):
    result = ""
    for i in range(start, idx):
        s = ""
        for j in constrained_obj:
            s += symbol + str(i) + "_" + str(j) + " "
        if relation == "eq":
            result += sum_counters_eq(s.strip(), value)
        elif relation == "le":
            result += sum_counters_le(s.strip(), value)
    return result

def introduction(params, rc, solver):
    result = ""
    if solver == "cvc4":
        result += "(set-logic LIA)\n"
        result += "(set-option :produce-models true)\n"
    result += parameters(params) + "\n"
    result += assertion(list_conjunction(rc)) + "\n"
    return result


def counter_constraints(start, idx, conf_symbol, trans_symbol, constraints):
    result = ""    
    for c in constraints:        
        if c['type'] == "configuration":
            result += add_constraint(start, idx + 1, conf_symbol, c['sum'], c['object'], c['result'])
        elif c['type'] == "transition":
            result += add_constraint(start, idx, trans_symbol, c['sum'], c['object'], c['result'])
        result += "\n"
    return result  


def assertion(assert_text):
    return "(assert\n" + assert_text + ")\n"

def initial_condition(initial, symbol, constraints):  
    result = "(and\n"
    init_constraints = [c for c in constraints if c['type'] == "configuration"]    
    for c in init_constraints:
        s = ""
        obj = [l for l in c['object'] if l in initial]
        for i in obj:
            s += " " + symbol + "0_" + str(i)
        if c['sum'] == "eq":
            result += sum_counters_eq(s.strip(), c['result'])
        elif c['sum'] == "le":
            result += sum_counters_le(s.strip(), c['result'])
    result += ")\n"
    return result  

def guards(start, idx1, rule_list, L, conf_symbol, trans_symbol):
    result = ""
    for i in range(start, idx1):        
        send_str = {}    
        for k in L:
            send_str[k] = ""
            for v in L[k]:
                send_str[k] += conf_symbol + str(i) + "_" + str(v) + " "
            if len(L[k]) > 1:
                send_str[k] = "(+ " + send_str[k].strip() + ")"
            else:
                send_str[k] = send_str[k].strip()
        for r in rule_list:        
            if r["guard"] != "true":
                grd = ""
                grd += "(not " + r["guard"] + ")"                
                snd = {k:v for (k,v) in L.items() if k in r["guard"]}
                for k in snd:
                    grd = grd.replace(k, send_str[k])
                result += "(=> " + grd + " (= " + trans_symbol + str(i) + "_" + str(r["idx"]) + " 0))\n"
        result += "\n"
    return result


def enabled(start, idx, local_list, rule_list, conf_symbol, trans_symbol):
    result = ""
    for i in range(start, idx):
        for j in local_list:
            rls = [r for r in rule_list if r["from"] == j]
            if len(rls) == 0:
                result += "(= 0 " + conf_symbol + str(i) + "_" + str(j) + ")\n"
            elif len(rls) == 1:
                result += "(= " + trans_symbol + str(i) + "_" + str(rls[0]["idx"]) + " " + conf_symbol + str(i) + "_" + str(j) + ")\n"
            else:
                rsum = "(+"
                for k in range(len(rls)):
                    rsum += " " + trans_symbol + str(i) + "_" + str(rls[k]["idx"])
                rsum += ")"
                result += "(= " + rsum + " " + conf_symbol + str(i) + "_" + str(j) + ")\n"
        result += "\n"
    return result

def effect(start, idx, local_list, rule_list, conf_symbol, trans_symbol):
    result = ""
    for i in range(start, idx):
        for j in local_list:
            rls = [r for r in rule_list if r["to"] == j]
            if len(rls) == 0:
                result += "(= 0 " + conf_symbol + str(i + 1) + "_" + str(j) + ")\n"
            elif len(rls) == 1:
                result += "(= " + trans_symbol + str(i) + "_" + str(rls[0]["idx"]) + " " + conf_symbol + str(i + 1) + "_" + str(j) + ")\n"
            else:
                rsum = "(+"
                for r in rls:
                    rsum += " " + trans_symbol + str(i) + "_" + str(r["idx"])
                rsum += ")"
                result += "(= " + rsum + " " + conf_symbol + str(i + 1) + "_" + str(j) + ")\n"
        result += "\n"
    return result

def diameter_query(start, diam, phase, length, local_list, rule_list, other_conf_symbol, conf_symbol, trans_symbol, constraints, L):
    result = "(forall ("
    for i in range(start, diam * phase + 1):
        for j in local_list:
            result += "(" + conf_symbol + str(i) + "_" + str(j) + " Int) "
        result += "\n"
        if i < diam * phase:
            for k in rule_list:
                result += "(" + trans_symbol + str(i) + "_" + str(k["idx"]) + " Int) "
        result += "\n"
    result = result.strip() + ")\n"
    result += "(=>\n(and\n"
    for i in local_list:
        result += "(= " + other_conf_symbol + "0_" + str(i) + " " + conf_symbol + "0_" + str(i) + ")\n"
    result += path_constraints(start, diam * phase, local_list, rule_list, conf_symbol, trans_symbol, constraints, L)    
    result += ")\n"
    result += diameter_conclusion(start, diam * phase + 1, phase, length, local_list, other_conf_symbol, conf_symbol)
    result += ")\n)\n"
    return result

def diameter_conclusion(start, end, phase, length, local_list, other_conf_symbol, conf_symbol):    
    result = "(and\n"
    for i in range(start, end):
        result += "(or\n"
        for j in local_list:
            result += "(not (= " + other_conf_symbol + str(length) + "_" + str(j) + " " + conf_symbol + str(i) + "_" + str(j) + "))\n" 
        result += ")\n"
    result += ")\n"    
    return result

def property_initial(symbol, init_str, L):
    result = init_str
    l = {k:v for (k,v) in L.items() if k in init_str}
    for k in l:
        s = ""
        for v in L[k]:
            s += symbol + "0_" + str(v) + " "
        if len(L[k]) > 1:
            s = "(+ " + s.strip() + ")"
        else:
            s = s.strip()
        result = result.replace(k, s)
    result += "\n"
    return result

def property_reachable(start, idx, phase, symbol, qf, reach_str, L):
    result = ""
    
    if qf == "all":
        result += "(and\n"
    elif qf == "some": 
        result += "(or\n"
    elif qf == "last":
        start = idx - 1

    l = {k:v for (k, v) in L.items() if k in reach_str}
    
    for i in range(start, idx, phase):
        s = reach_str
        send_str = {}
        for k in l:
            send_str[k] = ""
            for v in L[k]:
                send_str[k] += symbol + str(i) + "_" + str(v) + " "
            if len(L[k]) > 1:
                send_str[k] = "(+ " + send_str[k].strip() + ")"
            else:
                send_str[k] = send_str[k].strip()

            s = s.replace(k, send_str[k])
        
        result += s + "\n"
    
    if qf != "last":
        result += ")\n" 
    
    return result

def property_check(start, idx, phase, symbol, p, L):
    result = ""
    if p['initial'] == "true":
        result += property_reachable(start, idx + 1, phase, symbol, p['qf'], p['reachable'], L)
    else:
        result = "(and\n"
        result += property_initial(symbol, p['initial'], L)
        result += property_reachable(start, idx + 1, phase, symbol, p['qf'], p['reachable'], L)
        result += ")\n"    
    return result

def path_constraints(start, end, local_list, rule_list, conf_symbol, trans_symbol, constraints, L):
    result = "(and\n"
    result += non_negative(start, end + 1, len(local_list), conf_symbol) + "\n"
    result += non_negative(start, end, len(rule_list), trans_symbol) + "\n"
    result += counter_constraints(start, end, conf_symbol, trans_symbol, constraints) + "\n"
    result += guards(start, end, rule_list, L, conf_symbol, trans_symbol) + "\n"
    result += enabled(start, end, local_list, rule_list, conf_symbol, trans_symbol) + "\n"
    result += effect(start, end, local_list, rule_list, conf_symbol, trans_symbol) + "\n"   
    result += ")\n"
    return result


def path(start, end, local_list, rule_list, conf_symbol, trans_symbol, constraints, L):
    result = ""    
    result += declare_constants(start, end + 1, len(local_list), conf_symbol) + "\n"
    result += declare_constants(start, end, len(rule_list), trans_symbol) + "\n"
    result += assertion(path_constraints(start, end, local_list, rule_list, conf_symbol, trans_symbol, constraints, L))    
    return result 


def clean_round(r, local_list, rule_list, conf_symbol, trans_symbol, constraints, L, r_constraint, phase):
    constants = ""
    result = ""
    round_constraint = ""
    constants += declare_constants(r + 1, r + phase, len(local_list), conf_symbol) + "\n" 
    constants += declare_constants(r, r + phase, len(rule_list), trans_symbol) + "\n"
    result += "(and\n"
    result += non_negative(r + 1, r + phase, len(local_list), conf_symbol) + "\n"
    result += non_negative(r, r + phase, len(rule_list), trans_symbol) + "\n"
    rule_constraints = [c for c in constraints if c['type'] == "transition"]
    result += counter_constraints(r, r + phase, conf_symbol, trans_symbol, rule_constraints) + "\n"
    result += guards(r, r + phase, rule_list, L, conf_symbol, trans_symbol) + "\n"
    result += enabled(r, r + phase, local_list, rule_list, conf_symbol, trans_symbol) + "\n"
    result += effect(r, r + phase, local_list, rule_list, conf_symbol, trans_symbol) + "\n"   

    for c in r_constraint:
        round_constraint += add_constraint(r + 1, r + phase + 1, "c", c['sum'], c['object'], c['result']) + "\n"

    result += round_constraint
    result += ")\n"
    return constants + assertion(result)