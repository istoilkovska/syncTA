import os
import sys
import bmc
import chain
import time

bounded_model_checking = bmc.bounded_model_checking
compute_bound = chain.compute_bound

alg_list = [alg[:-3] for alg in os.listdir("boundable") if alg[-3:] == ".py" and alg[0] != "_"]

solver = ""
length = 0

if len(sys.argv) != 2:
    print("Usage: python run_boundable.py 'solver'")
    exit()
else:
    solver = sys.argv[1].strip()
    if solver != "cvc4" and solver != "z3":
        print("Currently the only supported solvers are cvc4 and z3") 
        exit()



output = open("output_boundable_" + solver + ".txt", "w")

output.write("Experimental results for bounded model checking with the " + solver + " SMT solver\n")
output.write("Boundable fragment\n\n")

for alg in alg_list:
    start_time = time.time()
    print("Checking " + alg + " with " + solver + " ...\n")
    output.write("Algorithm " + alg + "\n")

    (Psi, c) = compute_bound(alg, "boundable")
    output.write("nr. of atomic guards:\t" + str(Psi) + "\n")
    output.write("longest chain:\t" + str(c) + "\n\n")

    output.write("bounded model checking results:\n")
    start = time.time()
    
    result = bounded_model_checking(alg, "boundable", solver, Psi * c)
    bmc_time = time.time() - start
    print(result)
    output.write(result)
    pretty_time = "%s%s" % (time.strftime("%H:%M:%S", time.gmtime(bmc_time)), str(bmc_time)[str(bmc_time).index("."):8])
    output.write("\ttime to check properties: \t" + pretty_time + "\n\n")

    print(alg + " done!\n\n")

output.close()
print("Results found in output_boundable_" +solver + ".txt\n")

