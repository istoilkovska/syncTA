import os
import sys
import diameter
import bmc
import time
import helper

compute_diameter = diameter.compute_diameter
bounded_model_checking = bmc.bounded_model_checking

# get list of erroneous encodings of the algorithms
alg_list = [alg[:-3] for alg in os.listdir("counterexamples") if alg[-3:] == ".py" and alg[0] != "_"]
alg_list.sort()
wrongRC = [alg for alg in alg_list if alg.startswith('rb') or alg.startswith('phase')]

# supported solvers
solvers = ['z3', 'cvc4']

def print_table(results):
    """
    Prints a table with the results of computing the
    diameter and bounded model checking of encodings that contain errors
    """
    
    header = ["algorithm".center(15), "error injected".center(40),
              "d, z3".center(5), "d, cvc4".center(5), 
              "t_d, z3".center(8), "t_d, cvc4".center(9), 
              "t_b, z3".center(9), "t_b, cvc4".center(9)]
    hline = ['-' * len(h) for h in header]
    
    print(' + '.join(hline))
    print(' | '.join(header))
    print(' + '.join(hline))

    for alg in wrongRC:
        row = []
        row.append(alg.center(len(header[0])))
        for i in range(len(results[alg])):
            row.append(results[alg][i].center(len(header[i + 1])))
        print(' | '.join(row))
        print(' + '.join(hline))

    print(' + '.join(hline))

    for alg in alg_list:
        if alg not in wrongRC:
            row = []
            row.append(alg.center(len(header[0])))
            for i in range(len(results[alg])):
                row.append(results[alg][i].center(len(header[i + 1])))
            print(' | '.join(row))
            print(' + '.join(hline))
    

def compute_results():
    """
    For each erroneous encoding of an algorithm and each solver, compute the diameter, and 
    check the safety properties using bounded model checking.
    Expect some properties to be violated.
    """
    result = {}

    for alg in alg_list:
        # type of error injected
        error = ""
        # time to compute the diameter
        t_d = {}
        # time to perform bounded model checking
        t_b = {}
        # computed diameter
        diam = {}
        if alg in wrongRC:
            error = "wrong RC, " + helper.getRC(alg, "counterexamples")
        else: 
            error = "clean round not enforced"
        for solver in solvers:
            print("Checking " + alg + " with " + solver + " ...\n")

            start = time.time()
            # compute the diameter
            diam[solver] = compute_diameter(alg, "counterexamples", solver, 0, 5)
            diam_time = time.time() - start
            t_d[solver] = "%s%s" % (time.strftime("%M:%S", time.gmtime(diam_time)), str(diam_time)[str(diam_time).index("."):4])

            if diam[solver] != -1:
                # if the diameter has been computed, print it and use it for bounded model checking
                print('Diameter: ' + str(diam[solver]))
                start = time.time()
                # apply bounded model checking. Some properties should be violated
                bmc_result = bounded_model_checking(alg, "counterexamples", solver, diam[solver])
                bmc_time = time.time() - start
                t_b[solver] = "%s%s" % (time.strftime("%M:%S", time.gmtime(bmc_time)), str(bmc_time)[str(bmc_time).index("."):4])

                print(bmc_result)
                
            else:                
                diam[solver] = '-'
                t_d[solver] = '-'
                t_b[solver] = '-'
                print('The diameter cannot be determined\n')
        
        # store the result as a row in the results table
        result[alg] = [error, str(diam['z3']), str(diam['cvc4']), t_d['z3'], t_d['cvc4'], t_b['z3'], t_b['cvc4']]
        
    print_table(result)    

if __name__ == "__main__":
    compute_results()
