import os
import sys
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
call_solver_bmc = helper.call_solver_bmc

def bounded_model_checking(algorithm, pkg, solver, diam):    
    """
    Applies bounded model checking given a diameter
    """
    alg = importlib.import_module("." + algorithm, package = pkg)

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
            result = call_solver_bmc(solver, file_name, properties)           

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
                result = call_solver_bmc(solver, file_name, properties)
    
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
    if len(sys.argv) < 5:
        print('Usage: python diameter.py $algorithm $package $solver $diameter')
        exit()
    alg = str(sys.argv[1])
    pkg = str(sys.argv[2])
    solver = str(sys.argv[3])
    diam = int(sys.argv[4])
    print(bounded_model_checking(alg, pkg, solver, diam))     