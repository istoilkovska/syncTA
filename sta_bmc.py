import os
import sys
import diameter
import bmc
import time
import helper

compute_diameter = diameter.compute_diameter
bounded_model_checking = bmc.bounded_model_checking

# get list of algorithms
alg_list = [alg[:-3] for alg in os.listdir("algorithms") if alg[-3:] == ".py" and alg[0] != "_"]
alg_list.sort()
boundable = [alg for alg in alg_list if alg.startswith('rb')]

# supported solvers
solvers = ['z3', 'cvc4']

def print_table(results):
    """
    Prints a table with the experimental results, 
    comparable to Table 2 on page 14 in the paper
    """
    
    header = ["algorithm".center(12), "|L|".center(5), 
              "|R|".center(5), "|Psi|".center(5), "RC".center(27),
              "d, z3".center(5), "d, cvc4".center(5), 
              "t_d, z3".center(8), "t_d, cvc4".center(8), 
              "t_b, z3".center(8), "t_b, cvc4".center(8),  
              "", "c".center(5), "t_b, z3".center(8), "t_b, cvc4".center(8)]
    hline = ['-' * len(h) for h in header]
    
    print ' + '.join(hline)
    print ' | '.join(header)
    print ' + '.join(hline)

    for alg in boundable:
        row = []
        row.append(alg.center(len(header[0])))
        for i in range(len(results[alg])):
            row.append(results[alg][i].center(len(header[i + 1])))
        print ' | '.join(row)
        print ' + '.join(hline)

    print ' + '.join(hline)

    for alg in alg_list:
        if alg not in boundable:
            row = []
            row.append(alg.center(len(header[0])))
            for i in range(len(results[alg])):
                row.append(results[alg][i].center(len(header[i + 1])))
            print ' | '.join(row)
            print ' + '.join(hline)
    
def compute_results():
    """
    For each algorithm and each solver, compute the diameter, and 
    check the safety properties using bounded model checking.
    For a class of algorithms for which we show that a theoretical
    bound exists, compute this bound, and again apply bounded model
    checking using this bound.
    """
    result = {}

    for alg in alg_list:
        # some statistics about the algorithm: number of local states, number or rules
        stats = helper.get_stats(alg, "algorithms")
        # resilitence condition of the algorithm
        RC = helper.getRC(alg, "algorithms")
        # time to compute the diameter
        t_d = {}
        # time to perform bounded model checking using the computed diameter
        t_b = {}
        # time to perform bounded model checking using the theoretical bound
        t_c = {}
        # computed diameter
        diam = {}
        if alg in boundable:
            # compute theoretical bound for a class of algorithms
            (Psi, c) = helper.compute_bound(alg, "algorithms")
        else: 
            c = '-'
        
        for solver in solvers:
            print("Checking " + alg + " with " + solver + " ...\n")

            start = time.time()
            # compute diameter
            diam[solver] = compute_diameter(alg, "algorithms", solver, 0, 5)
            diam_time = time.time() - start
            t_d[solver] = "%s%s" % (time.strftime("%M:%S", time.gmtime(diam_time)), str(diam_time)[str(diam_time).index("."):4])

            if diam[solver] != -1:
                # if the diameter has been computed, print it and use it for bounded model checking
                print 'Diameter: ' + str(diam[solver])
                start = time.time()
                # apply bounded model checking to check correctness of properties
                bmc_result = bounded_model_checking(alg, "algorithms", solver, diam[solver])
                bmc_time = time.time() - start
                t_b[solver] = "%s%s" % (time.strftime("%M:%S", time.gmtime(bmc_time)), str(bmc_time)[str(bmc_time).index("."):4])

                if alg in boundable:
                    # apply bounded model checking with the theoretical bound for a class of algorithms
                    start = time.time()    
                    bmc_result = bounded_model_checking(alg, "algorithms", solver, Psi * c)
                    bmc_time = time.time() - start
                    t_c[solver] = "%s%s" % (time.strftime("%M:%S", time.gmtime(bmc_time)), str(bmc_time)[str(bmc_time).index("."):4])
                else:
                    t_c[solver] = '-'

                print bmc_result        
            else:
                diam[solver] = '-'
                t_d[solver] = '-'
                t_b[solver] = '-'
                print 'The diameter cannot be determined\n'

        # store the result as a row in the results table
        result[alg] = [str(stats['L']), str(stats['R']), str(stats['Psi']), RC, str(diam['z3']), str(diam['cvc4']), t_d['z3'], t_d['cvc4'], t_b['z3'], t_b['cvc4'], "", str(c), t_c['z3'], t_c['cvc4']]

    print_table(result)    

if __name__ == "__main__":
    compute_results()
