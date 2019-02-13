import os
import sys
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
clean_round = helper.clean_round

def bounded_model_checking(algorithm, pkg, solver, diam):    
    """
    Applies bounded model checking given a diameter
    """
	
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

    maxlength = diam 

    result = {}
    for p in properties:
        result[p['name']] = []

	# check whether a clean round has to be imposed
    if round_constraint == []: 
		# if not, check paths with (length) many transitions
        for length in range(phase, maxlength + 1, phase):
            
            smt_file = open(file_name, "w")
            # create a path, with (length) many transitions
            smt_path = path(0, length, local, rules, "c", "t", constraints, L)
	    	# impose initial conditions
            smt_path += assertion(initial_condition(initial, "c", constraints)) 
        
            smt_file.write(intro)    
            smt_file.write(smt_path)
						
			# add assertions for each property
            for p in properties:
                s = ""
                s += assertion(property_check(0, length, phase, "c", p, L)) + "\n"
                s = "(push)\n" + s + "(check-sat)\n" + "(pop)\n"
                smt_file.write(s)
            
            smt_file.close()

			# check the properties using cvc4 or z3
            if solver == "cvc4":
                smt = subprocess.Popen(["cvc4", "--lang", "smt2", "--incremental", file_name], stdout=subprocess.PIPE)
            elif solver == "z3":
                smt = subprocess.Popen(["z3", "-smt2", file_name], stdout=subprocess.PIPE)
            
            output = smt.communicate()[0]
            results = output.split()
    
            if len(results) == len(properties):
                for i in range(len(results)):
                    if results[i] == "unsat" or results[i] == "sat":
                        result['' + properties[i]["name"]].append(results[i])
                    else:
                        result['' + properties[i]["name"]].append('no result')
            else:
                print("SMT solver reported an error")
                exit()
            

    else:
		# if a clean round has to be imposed, check paths with at most (2 * length) transitions
        for length1 in range(phase, maxlength  + 1, phase):
            for length2 in range(phase, maxlength  + 1, phase):
                # total = length1 + length2 + phase
                total = length1 + length2

                smt_file = open(file_name, "w")
            
				# create a path with (length1 + length2) transitions
                smt_path = path(0, total, local, rules, "c", "t", constraints, L)
                smt_path += assertion(initial_condition(initial, "c", constraints)) 
        
                smt_file.write(intro)    
                
                # impose clean round constraint
                smt_path += clean_round(length1 - phase, local, rules, "c", "t", constraints, L, round_constraint, phase) + "\n"
                

                smt_file.write(smt_path)

				# add assertions for each property
                for p in properties:
                    s = ""
                    s += assertion(property_check(0, total, phase, "c", p, L)) + "\n"
                    s = "(push)\n" + s + "(check-sat)\n" + "(pop)\n"
                    smt_file.write(s)
                
                smt_file.close()

				# check the properties using cvc4 or z3
                if solver == "cvc4":
                    smt = subprocess.Popen(["cvc4", "--lang", "smt2", "--incremental", file_name], stdout=subprocess.PIPE)
                elif solver == "z3":
                    smt = subprocess.Popen(["z3", "-smt2", file_name], stdout=subprocess.PIPE)
    
                output = smt.communicate()[0]
                results = output.split()
        
                if len(results) == len(properties):
                    for i in range(len(results)):
                        if results[i] == "unsat" or results[i] == "sat":
                            result['' + properties[i]["name"]].append(results[i])
                        else:
                            result['' + properties[i]["name"]].append('no result')
                else:
                    print("SMT solver reported an error")
                    exit()
    
    str_result = ""
    for p in properties:
        lres = result[p['name']]
        
        if 'sat' in lres:
            str_result += p['name'] + " is violated\n"
        elif 'unsat' not in lres:
            str_result += p['name'] + " cannot be checked\n"
        else:
            str_result += p['name'] + " holds\n"

    
    return str_result

if __name__ == "__main__":
    algorithm = sys.argv[1]
    pkg = sys.argv[2]
    solver = sys.argv[3]
    diam = int(sys.argv[4])
    print bounded_model_checking(algorithm, pkg, solver, diam)