import importlib
import subprocess

def new_constant(const_name):
    """
    Returns an SMT command to declare a new integer constant
    """
    return "(declare-const " + const_name + " Int)\n"

def parameters(params):
    """
    Declare the parameters as constants
    """
    result = ""
    for p in params:  
        result += new_constant(p)
    return result

def declare_constants(start, idx1, idx2, symbol):
    """
    Declare constants for configurations/transitions
    """
    result = ""
    for i in range(start, idx1):
        for j in range(idx2):
            const_name = symbol + str(i) + "_" + str(j)
            result += new_constant(const_name)
    return result

def list_conjunction(l):
    """
    Returns an SMT conjunction, given a list of conjuncts
    """
    result = "(and"
    for item in l:
        result += " " + item
    result += ")\n"
    return result

def sum_counters_eq(sum_cnt, num):
    """
    Returns an SMT equality assertion given a list of counters and a threshold
    """
    return "(= (+ " + sum_cnt + ") " + str(num) + ")\n"

def sum_counters_le(sum_cnt, num):
    """
    Returns an SMT inequality assertion given a list of counters and a threshold
    """
    return "(<= (+ " + sum_cnt + ") " + str(num) + ")\n"

def non_negative(start, idx1, idx2, symbol):
    """
    Returns SMT constrains about constants being non-negative
    """
    result = ""
    for i in range(start, idx1):
        for j in range(idx2):
            const_name = symbol + str(i) + "_" + str(j)
            result += "(>= " + const_name + " 0)\n"
    return result

def add_constraint(start, idx, symbol, relation, constrained_obj, value):
    """
    Returns an inequality or equality constraint on a configuration or transition 
    """
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
    """
    First lines of the SMT file
    """
    result = ""
    if solver == "cvc4":
        result += "(set-logic LIA)\n"
        result += "(set-option :produce-models true)\n"
    result += parameters(params) + "\n"
    result += assertion(list_conjunction(rc)) + "\n"
    return result


def counter_constraints(start, idx, conf_symbol, trans_symbol, constraints):
    """
    Returns SMT constrains that define the bounds of the counters and transitions
    """    
    result = ""    
    for c in constraints:        
        if c['type'] == "configuration":
            result += add_constraint(start, idx + 1, conf_symbol, c['sum'], c['object'], c['result'])
        elif c['type'] == "transition":
            result += add_constraint(start, idx, trans_symbol, c['sum'], c['object'], c['result'])
        result += "\n"
    return result  


def assertion(assert_text):
    """
    Returns an SMT assertion
    """
    return "(assert\n" + assert_text + ")\n"

def initial_condition(initial, symbol, constraints):  
    """
    Returns the initial constrains defining initial states of the counter system 
    """
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
    """
    Returns SMT constraints stating that disabled guards have zero factors in a transition
    """
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
    """
    Returns SMT constrains that relate a configuration and a transition applied to it
    """
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
    """
    Returns SMT constrains that relate a transition and a configuration 
    obtained as a result of the transition
    """
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
    """
    Generates the diameter query
    """
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
    """
    Conclusion of the diameter query
    """  
    result = "(and\n"
    for i in range(start, end):
        result += "(or\n"
        for j in local_list:
            result += "(not (= " + other_conf_symbol + str(length) + "_" + str(j) + " " + conf_symbol + str(i) + "_" + str(j) + "))\n" 
        result += ")\n"
    result += ")\n"    
    return result

def property_initial(symbol, init_str, L):
    """
    Returns SMT constraints that need to hold initially for a property to hold
    """
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
    """
    Returns SMT constrains stating that a configuration is reachable
    """
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
    """
    Generates SMT constraints needed to check a property of an algorithm
    """
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
    """
    Returns SMT constraints that need to hold on each path of the counter system
    """
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
    """
    Declares SMT constants and generates SMT constraints for a path in the counter system
    """
    result = ""    
    result += declare_constants(start, end + 1, len(local_list), conf_symbol) + "\n"
    result += declare_constants(start, end, len(rule_list), trans_symbol) + "\n"
    result += assertion(path_constraints(start, end, local_list, rule_list, conf_symbol, trans_symbol, constraints, L))    
    return result 


def clean_round_config(r, local_list, rule_list, conf_symbol, trans_symbol, constraints, L, r_constraint, phase):
    """
	Generates the clean round constraint imposed on a configuration
	"""
    constants = ""
    result = ""
    round_constraint = ""
    result += "(and\n"
    for c in r_constraint:
        round_constraint += add_constraint(r + 1, r + phase + 1, conf_symbol, c['sum'], c['object'], c['result']) + "\n"

    result += round_constraint
    result += ")\n"
    return constants + assertion(result)

def clean_round_trans(r, local_list, rule_list, conf_symbol, trans_symbol, constraints, L, r_constraint, phase):
    """
	Generates the clean round constraint imposed on a transition
	"""
    constants = ""
    result = ""
    round_constraint = ""

    send_str = {}    
    for k in L:
        send_str[k] = ""
        for v in L[k]:
            send_str[k] += conf_symbol + str(r) + "_" + str(v) + " "
        if len(L[k]) > 1:
            send_str[k] = "(+ " + send_str[k].strip() + ")"
        else:
            send_str[k] = send_str[k].strip()

    result += "(and\n"
    for c in r_constraint:
        pre = c['pre']
        snd = {k:v for (k,v) in L.items() if k in pre}
        for k in snd:
            pre = pre.replace(k, send_str[k])
        constraint = add_constraint(r + 1, r + phase + 1, trans_symbol, c['sum'], c['object'], c['result'])     
        round_constraint += "(=> {} {})\n".format(pre, constraint)

    result += round_constraint
    result += ")\n"
    return constants + assertion(result)


def compute_sub(guard_str):
    """
    Given a guard, return its sub-guards
    """
    parens = []
    sub = []
    for i in range(len(guard_str)):        
        if guard_str[i] == '(':
            parens.append(i)
        if guard_str[i] == ')':
            j = parens.pop()
            g = guard_str[j:i + 1].strip()
            if g.startswith('(+') or g.startswith('(-') or g.startswith('(*'):
                continue            
            sub.append(g)
    return sub

def compute_atomic(guards):
    """
    Returns a list of atomic guards
    """
    atomic = []
    for g in guards:
        a = []
        if str(g).startswith('(and ') or str(g).startswith('(not '):
            a = compute_sub(g[5:-1])            
        elif str(g).startswith('(or '):
            a = compute_sub(g[4:-1])
        else:
            if g not in atomic and g != 'true':
                atomic.append(g)                
        for x in a:
            guards.append(x)

    return atomic

def compute_graph(local, rules):
    """
    Obtain a DAG given an STA
    """
    graph = {}
    for l in local:
        graph[l] = [r['to'] for r in rules if r['from'] == l and r['to'] != r['from']]
    return graph

def dfs(graph, vertex, explored=None, path=None):
    """
    Depth first search to compute length of the paths in the graph starting from vertex
    """
    if explored == None:
        explored = []
    if path == None:
        path = 0

    explored.append(vertex)

    len_paths = []
    for w in graph[vertex]:
        if w not in explored:
            new_path = path + 1
            len_paths.append(new_path)
            len_paths.extend(dfs(graph, w, explored[:], new_path))

    return len_paths

def longest_path(graph, initial):
    """
    Returns the length of the longest path in the graph
    """
    max_len = 0
    for i in initial:
        max_i = max(dfs(graph, i))
        if max_len < max_i:
            max_len = max_i
    return max_len

def compute_bound(algorithm, pkg):
    """
    Computes the theoretical bound on the diameter for a class of algorithms
    """
    alg = importlib.import_module("." + algorithm, package=pkg)

    guards = [r['guard'] for r in alg.rules]
    atomic = compute_atomic(guards)
    Psi = len(atomic)
    graph = compute_graph(alg.local, alg.rules)
    c = longest_path(graph, alg.initial)

    return (Psi, c)



def get_stats(algorithm, pkg):
    """
    Returns statistics about the algorithm: 
        - number of local states
        - number of rules
        - number of atomic guards
    """
    alg = importlib.import_module("." + algorithm, package = pkg)
    
    stats = {}
    stats['L'] = len(alg.local)
    stats['R'] = len(alg.rules)
    guards = [r['guard'] for r in alg.rules]
    stats['Psi'] = len(compute_atomic(guards))
    return stats

def getRC(algorithm, pkg):
    """
    Returns the resilience condition of the algorithm
    """
    alg = importlib.import_module("." + algorithm, package = pkg)
    RC = alg.rc[-1]
    
    return RC

def call_solver(solver, file_name, timeout):
    cvc4_timeout = timeout * 1000
    if solver == "cvc4":
        smt = subprocess.Popen(["cvc4", "--lang", "smt2", "--incremental", "--tlimit={}".format(str(cvc4_timeout)), file_name], stdout=subprocess.PIPE)
    elif solver == "z3":
        smt = subprocess.Popen(["z3", "-smt2", "-T:{}".format(timeout), file_name], stdout=subprocess.PIPE)
    
    try: 
        output = smt.communicate()[0]
    except:
        smt.kill()
        print("Couldn't get output from the SMT solver")
        return -1, "error"

    if isinstance(output, bytes):
        output = output.decode('utf-8')

    if output == "timeout":
        return -1, "timeout"    

    return 0, output.strip()
