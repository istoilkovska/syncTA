import os
import sys
import diameter
import bmc
import time
import helper

compute_diameter = diameter.compute_diameter
bounded_model_checking = bmc.bounded_model_checking

alg_list = [alg[:-3] for alg in os.listdir("counterexamples") if alg[-3:] == ".py" and alg[0] != "_"]
alg_list.sort()
wrongRC = [alg for alg in alg_list if alg.startswith('rb') or alg.startswith('phase')]

solvers = ['z3', 'cvc4']

def print_table(results):
    
    header = ["algorithm".center(15), "error injected".center(40),
              "d, z3".center(5), "d, cvc4".center(5), 
              "t_d, z3".center(7), "t_d, cvc4".center(7), 
              "t_b, z3".center(7), "t_b, cvc4".center(7)]
    hline = ['-' * len(h) for h in header]
    
    print ' + '.join(hline)
    print ' | '.join(header)
    print ' + '.join(hline)

    for alg in wrongRC:
        row = []
        row.append(alg.center(len(header[0])))
        for i in range(len(results[alg])):
            row.append(results[alg][i].center(len(header[i + 1])))
        print ' | '.join(row)
        print ' + '.join(hline)

    print ' + '.join(hline)

    for alg in alg_list:
        if alg not in wrongRC:
            row = []
            row.append(alg.center(len(header[0])))
            for i in range(len(results[alg])):
                row.append(results[alg][i].center(len(header[i + 1])))
            print ' | '.join(row)
            print ' + '.join(hline)
    

def compute_results():
    result = {}

    for alg in alg_list:
        error = ""
        t_d = {}
        t_b = {}
        diam = {}
        if alg in wrongRC:
            error = "wrong RC, " + helper.getRC(alg, "counterexamples")
        else: 
            error = "clean round not enforced"
        for solver in solvers:
            print("Checking " + alg + " with " + solver + " ...\n")

            start = time.time()
            diam[solver] = compute_diameter(alg, "counterexamples", solver, 0, 5)
            diam_time = time.time() - start
            t_d[solver] = "%s%s" % (time.strftime("%S", time.gmtime(diam_time)), str(diam_time)[str(diam_time).index("."):4])

            if diam[solver] != -1:
                start = time.time()
                bmc_result = bounded_model_checking(alg, "counterexamples", solver, diam[solver])
                bmc_time = time.time() - start
                t_b[solver] = "%s%s" % (time.strftime("%S", time.gmtime(bmc_time)), str(bmc_time)[str(bmc_time).index("."):4])

                print bmc_result      
                
            else:                
                diam[solver] = '-'
                t_d[solver] = '-'
                t_b[solver] = '-'
                print 'The diameter cannot be determined\n'  

        result[alg] = [error, str(diam['z3']), str(diam['cvc4']), t_d['z3'], t_d['cvc4'], t_b['z3'], t_b['cvc4']]
        


    print_table(result)    

if __name__ == "__main__":
    compute_results()
