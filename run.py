import os
import sys
import diameter
import bmc
import time

compute_diameter = diameter.compute_diameter
bounded_model_checking = bmc.bounded_model_checking

alg_list = [alg[:-3] for alg in os.listdir("algorithms") if alg[-3:] == ".py" and alg[0] != "_"]

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

output.write("Experimental results for bounded model checking with the " + solver + " SMT solver\n\n")

for alg in alg_list:
    start_time = time.time()
    print("Checking " + alg + " with " + solver + " ...\n")
    output.write("Algorithm " + alg + "\n")

    start = time.time()
    diam = compute_diameter(alg, solver, 0, 5)
    diam_time = time.time() - start
    print("Diameter " + str(diam) + "\n")
    print(diam_time)
    pretty_time = "%s%s" % (time.strftime("%M:%S", time.gmtime(diam_time)), str(diam_time)[str(diam_time).index("."):])
    output.write("diameter: \t" + str(diam) + "\n\ttime to compute diameter: \t" + pretty_time + "\n\n")

    output.write("bounded model checking results:\n")
    start = time.time()
    result = bounded_model_checking(alg, solver, diam)
    bmc_time = time.time() - start
    print(result)
    output.write(result)
    pretty_time = "%s%s" % (time.strftime("%M:%S", time.gmtime(bmc_time)), str(bmc_time)[1:])
    output.write("\ttime to check properties: \t" + pretty_time + "\n")

    total_time = time.time() - start_time
    pretty_time = "%s%s" % (time.strftime("%M:%S", time.gmtime(total_time)), str(total_time)[1:])
    output.write("\ttotal time: \t\t\t\t" + pretty_time + "\n\n\n")

    print(alg + " done!\n\n")

output.close()
print("Results found in output_" +solver + ".txt\n")



