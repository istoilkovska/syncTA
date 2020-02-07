import os
import sys
import importlib
import subprocess
import helper

introduction = helper.introduction
assertion = helper.assertion
initial_condition = helper.initial_condition
diameter_query = helper.diameter_query
path = helper.path
call_solver_diameter = helper.call_solver_diameter

def compute_diameter(algorithm, pkg, solver, start, end):
    """
    Computes the diameter of a given algorithm
    """

    alg = importlib.import_module("." + algorithm, package = pkg)

    local = alg.local
    params = alg.params
    rc = alg.rc
    rules = alg.rules
    initial = alg.initial
    L = alg.L
    constraints = alg.constraints
    phase = alg.phase

    
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    subdir = os.path.join(file_dir, "smt", "diameter")
    if not os.path.isdir(subdir):
		    os.makedirs(subdir)
    file_name = os.path.join(subdir, algorithm + "_diam.smt")

    intro = introduction(params, rc, solver)    

    for diam in range(start, end): 
        if diam == 0:
            continue

        length = diam * phase + phase
        
        smt_path = ""    
        smt_formula = ""

        smt_file = open(file_name, "w")      
        
		# declare a path of length diam * phase + phase 
        smt_path += path(0, length, local, rules, "c", "t", constraints, L)

        if phase > 1:
            smt_path += assertion(initial_condition(initial, "c", constraints))

		# check if all configurations on a path of length diam * phase, 
        # starting in the same initial configuration as the above path,
        # are different than the last reachable state of the above path
        smt_formula = assertion(diameter_query(0, diam, phase, length, local, rules, "c", "d", "r", constraints, L))

        smt_file.write(intro)
        smt_file.write(smt_path)
        smt_file.write(smt_formula)     
        smt_file.write("(check-sat)") 
        smt_file.close()

		# use cvc4 or z3 to check for unsat
        result = call_solver_diameter(solver, file_name)
        if result == "unsat":
            break
        elif result == "unknown":
            print("Timeout")
            return -1

    if result == "sat":
        print("The diameter is not between " + str(start) + " and " + str(end))
        return -1

    return diam * phase

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('Usage: python diameter.py $algorithm $package $solver')
        exit()
    alg = str(sys.argv[1])
    pkg = str(sys.argv[2])
    solver = str(sys.argv[3])
    print('Computing diameter for ' + alg + ' using ' + solver + '...')
    diam = compute_diameter(alg, pkg, solver, 0, 6)
    if diam != -1:
        print('Diameter: ' + str(diam))
    else:
        print('The diameter cannot be computed.')