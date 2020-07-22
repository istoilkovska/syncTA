import os
import sys
import diameter
import bmc
import time
import translateSTA

alg_list = [alg[3:-3] for alg in os.listdir("receiveSTA") if alg[-3:] == ".py" and alg[0] != "_"]
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

output.write("Experimental results for receive STA translation\n")
output.write("Translation done using Z3\n\n")

for alg in alg_list:
    print("Translating receive STA of " + alg + " to STA...\n")
    start = time.time()
    translateSTA.translateSTA(alg)
    translate_time = time.time() - start
    pretty_time = "%s%s" % (time.strftime("%H:%M:%S", time.gmtime(translate_time)), str(translate_time)[str(translate_time).index("."):8])
    output.write("time to translate receive STA to STA: \t" + pretty_time + "\n\n")

    print("Checking implication of guards between generated STA and manual STA of " + alg + "... ")
    start = time.time()
    result = translateSTA.check_implication(alg)
    check_time = time.time() - start
    pretty_time = "%s%s" % (time.strftime("%H:%M:%S", time.gmtime(translate_time)), str(translate_time)[str(translate_time).index("."):8])
    output.write("time to translate receive STA to STA: \t" + pretty_time + "\n\n")



output.write("Experimental results for bounded model checking of the translated STA with the " + solver + " SMT solver\n")
output.write("Diameter computed using SMT solver\n\n")

for alg in alg_list:
    print("Checking the translated STA of " + alg + " with " + solver + " ...\n")
    output.write("Algorithm " + alg + "\n")

    snd_alg = 'snd_{}'.format(alg)
    start = time.time()
    diam = compute_diameter(snd_alg, "sendSTA", solver, 0, 5)
    diam_time = time.time() - start
    print("Diameter " + str(diam) + "\n")
    pretty_time = "%s%s" % (time.strftime("%H:%M:%S", time.gmtime(diam_time)), str(diam_time)[str(diam_time).index("."):8])
    output.write("diameter: \t" + str(diam) + "\n\ttime to compute diameter: \t" + pretty_time + "\n\n")

    output.write("bounded model checking results:\n")
    start = time.time()
    result = bounded_model_checking(snd_alg, "sendSTA", solver, diam)
    bmc_time = time.time() - start
    print(result)
    output.write(result)
    pretty_time = "%s%s" % (time.strftime("%H:%M:%S", time.gmtime(bmc_time)), str(bmc_time)[str(bmc_time).index("."):8])
    output.write("\ttime to check properties: \t" + pretty_time + "\n\n")

    print(alg + " done!\n\n")

output.close()
print("Results found in output_" +solver + ".txt\n")



