import os
import sys
import diameter
import bmc
import time
import translate_sta

alg_list = [alg[4:-3] for alg in os.listdir("receiveSTA") if alg[-3:] == ".py" and alg[0] != "_"]
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
    print('Processing {}...'.format(alg))
    output.write("Algorithm " + alg + "\n")
    
    print('Translating receive STA of {}...'.format(alg))
    start = time.time()
    snd_file_name = translate_sta.translate_sta(alg)
    translate_time = time.time() - start
    pretty_time = '{}{}'.format(time.strftime("%H:%M:%S", time.gmtime(translate_time)), str(translate_time)[str(translate_time).index("."):8])
    print('Translation stored in {}'.format(snd_file_name))
    output.write('Translation to STA stored in {}\n'.format(snd_file_name))
    output.write('Time to translate receive STA to STA: \t{}\n\n'.format(pretty_time))


    print("Checking implication of guards between generated STA and manual STA of " + alg + "... ")
    start = time.time()
    result = translate_sta.check_implication(alg)
    check_time = time.time() - start
    pretty_time = '{}{}'.format(time.strftime("%H:%M:%S", time.gmtime(check_time)), str(check_time)[str(check_time).index("."):8])
    if result != -1:
        print('Guard implication: {} of the guards of the generated STA imply the guards of the manual STA'.format(result))
        output.write('Guard implication: {} of the guards of the generated STA imply the guards of the manual STA\n'.format(result))
    else:
        print('There was an error in checking the guard implications.')
        output.write('There was an error in checking the guard implications.\n')
    output.write('Time to check implication of guards between generated STA and manual STA: \t{}\n\n'.format(pretty_time))

    if alg == 'kset_omit2':
        print('Skipping bounded model checking for {}, due to a timeout in the computation of the diameter.'.format(alg))
        output.write('Skipping bounded model checking for {}, due to a timeout in the computation of the diameter.\n'.format(alg))

        print('To check it separately, run: python.py diameter.py snd_kset_omit2 sendSTA $solver\n\n')
        continue

    output.write("Experimental results for bounded model checking of the translated STA with the " + solver + " SMT solver\n")
    print("Checking the translated STA of " + alg + " with " + solver + " ...\n")
    snd_alg = 'snd_{}'.format(alg)
    start = time.time()
    err, diam = diameter.compute_diameter(snd_alg, "sendSTA", solver, 0, 5)
    diam_time = time.time() - start
    print("Diameter " + str(diam) + "\n")
    pretty_time = "%s%s" % (time.strftime("%H:%M:%S", time.gmtime(diam_time)), str(diam_time)[str(diam_time).index("."):8])
    output.write("diameter: \t" + str(diam) + "\n\ttime to compute diameter: \t" + pretty_time + "\n\n")

    output.write("Bounded model checking results:\n")
    start = time.time()
    err, result = bmc.bounded_model_checking(snd_alg, "sendSTA", solver, diam)
    bmc_time = time.time() - start
    print(result)
    output.write(result)
    pretty_time = "%s%s" % (time.strftime("%H:%M:%S", time.gmtime(bmc_time)), str(bmc_time)[str(bmc_time).index("."):8])
    output.write("\ttime to check properties: \t" + pretty_time + "\n\n\n")

    print(alg + " done!\n\n")

output.close()
print("Results found in output_" +solver + ".txt\n")



