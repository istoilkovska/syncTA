import os
import subprocess
import helper
import importlib
import math
import diameter

introduction = helper.introduction
assertion = helper.assertion
initial_condition = helper.initial_condition
property_check = helper.property_check
path = helper.path
magic_round = helper.magic_round

def bounded_model_checking(algorithm, pkg, solver, diam):    

    alg = importlib.import_module("." + algorithm, package=pkg)

    local = alg.local
    params = alg.params
    rc = alg.rc
    rules = alg.rules
    initial = alg.initial
    L = alg.L
    constraints = alg.constraints
    properties = alg.properties
    phase = alg.phase


    file_dir = os.path.dirname(os.path.realpath('__file__'))
    subdir = os.path.join(file_dir, "smt", "bmc")
    if not os.path.isdir(subdir):
		    os.makedirs(subdir)
    file_name = os.path.join(subdir, algorithm + "_bmc.smt")

    smt_file = open(file_name, "w")

    intro = introduction(params, rc, solver)

    round_constraint = [c for c in constraints if c['type'] == "round"]

    length = diam * phase

    smt_path = path(0, length, local, rules, "c", "t", constraints, L)
    smt_path += assertion(initial_condition(initial, "c", constraints))
    
    smt_file.write(intro)

    

    if round_constraint != []:    
        smt_path += path(length + phase, 2 * length + phase, local, rules, "c", "t", constraints, L)
        smt_path += magic_round(length, local, rules, "c", "t", constraints, L, round_constraint, phase) + "\n"
        
        length = 2 * length + phase
        
    smt_file.write(smt_path)

    for p in properties:
        s = ""
        s += assertion(property_check(0, length, phase, "c", p, L)) + "\n"
        s = "(push)\n" + s + "(check-sat)\n" + "(pop)\n"
        smt_file.write(s)
        
    smt_file.close()

    if solver == "cvc4":
        smt = subprocess.Popen(["cvc4", "--lang", "smt2", "--incremental", file_name], stdout=subprocess.PIPE)
    elif solver == "z3":
        smt = subprocess.Popen(["z3", "-smt2", file_name], stdout=subprocess.PIPE)
    elif solver == "vampire":
        smt = subprocess.Popen(["vampire", "--input-syntax", "smtlib2", file_name], stdout=subprocess.PIPE)

    output = smt.communicate()[0]
    
    result = ""
    results = output.split()
    if len(results) == len(properties):
        for i in range(len(results)):
            if results[i] == "unsat":
                result += properties[i]["name"] + " holds\n"
            elif results[i] == "sat":
                result += properties[i]["name"] + " is violated\n"
            else:
                result += properties[i]["name"] + " cannot be checked\n"
    else:
        result = "SMT solver reported an error\n"
    return result
