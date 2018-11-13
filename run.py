import os
import sys
import diameter
import bmc
import time

compute_diameter = diameter.compute_diameter
bounded_model_checking = bmc.bounded_model_checking

alg_list = [alg[:-3] for alg in os.listdir("algorithms") if alg[-3:] == ".py" and alg[0] != "_"]
alg_list.sort()

solver = ""

if len(sys.argv) != 2:
    print("Usage: python run.py 'solver'")
    exit()
else:
    solver = sys.argv[1].strip()
    if solver != "cvc4" and solver != "z3":
        print("Currently the only supported solvers are cvc4 and z3") 
        exit()



output = open("output_" + solver + ".txt", "w")

output.write("Experimental results for bounded model checking with the " + solver + " SMT solver\n")
output.write("Diameter computed using SMT solver\n\n")

for alg in alg_list:
    print("Checking " + alg + " with " + solver + " ...\n")
    output.write("Algorithm " + alg + "\n")

    start = time.time()
    diam = compute_diameter(alg, "algorithms", solver, 0, 5)
    diam_time = time.time() - start
    print("Diameter " + str(diam) + "\n")
    pretty_time = "%s%s" % (time.strftime("%H:%M:%S", time.gmtime(diam_time)), str(diam_time)[str(diam_time).index("."):8])
    output.write("diameter: \t" + str(diam) + "\n\ttime to compute diameter: \t" + pretty_time + "\n\n")

    output.write("bounded model checking results:\n")
    start = time.time()
    result = bounded_model_checking(alg, "algorithms", solver, diam)
    bmc_time = time.time() - start
    print(result)
    output.write(result)
    pretty_time = "%s%s" % (time.strftime("%H:%M:%S", time.gmtime(bmc_time)), str(bmc_time)[str(bmc_time).index("."):8])
    output.write("\ttime to check properties: \t" + pretty_time + "\n\n")

    print(alg + " done!\n\n")

output.close()
print("Results found in output_" +solver + ".txt\n")



