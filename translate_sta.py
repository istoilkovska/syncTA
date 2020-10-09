import parsing
import os
import sys
import generate_sta

def translate_sta(benchmark):
    file_dir = os.path.dirname(os.path.realpath('__file__'))
      
    rcv_subdir = os.path.join(file_dir, 'receiveSTA')
    if not os.path.isdir(rcv_subdir):
        print('No receive STA found.')
        return -1

    snd_subdir = os.path.join(file_dir, 'sendSTA')
    if not os.path.isdir(snd_subdir):
        os.makedirs(snd_subdir)
    snd_file_name = os.path.join(snd_subdir, '{}{}{}'.format('snd_', benchmark, '.py'))    

    algorithm = 'rcv_{}'.format(benchmark)
    # get locations, initial locations, rules
    locations = parsing.get_locations(algorithm, 'receiveSTA')
    init_locations = parsing.get_init_locations(algorithm, 'receiveSTA')
    rcv_rules = parsing.get_rules(algorithm, 'receiveSTA')    

    # get sent and received message counters
    snd_counters = parsing.get_snd_counters(algorithm, 'receiveSTA')
    L = parsing.get_L(algorithm, 'receiveSTA')
    rcv_counters = parsing.get_rcv_counters(algorithm, 'receiveSTA')

    # get parameters, resilience condition, environment assumption, and phase
    parameters = parsing.get_parameters(algorithm, 'receiveSTA')
    res_cond = parsing.get_resilience_condition(algorithm, 'receiveSTA')
    constraints = parsing.get_constraints(algorithm, 'receiveSTA')
    rcv_environment = parsing.get_environment(algorithm, 'receiveSTA')
    phase = parsing.get_phase(algorithm, 'receiveSTA')

    # get properties
    properties = parsing.get_properties(algorithm, 'receiveSTA')

    # eliminate receive message counters from rules
    rules = generate_sta.translate_rules(algorithm, rcv_rules, parameters, res_cond, rcv_counters, snd_counters, rcv_environment)

    generate_sta.write_sndta(snd_file_name, locations, L, init_locations, rules, parameters, res_cond, constraints, phase, properties)

    return snd_file_name


def check_implication(benchmark):

    generated_rules = parsing.get_rules('snd_{}'.format(benchmark), 'sendSTA')
    manual_rules = parsing.get_rules(benchmark, 'algorithms')

    generated_guards = {gr['idx']:gr['guard'] for gr in generated_rules}
    manual_guards = {mr['idx']:mr['guard'] for mr in manual_rules}

    snd_vars = parsing.get_snd_counters(benchmark, 'algorithms')
    parameters = parsing.get_parameters(benchmark, 'algorithms')
    res_cond = parsing.get_resilience_condition(benchmark, 'algorithms')

    if len(generated_guards) != len(manual_guards):
        print('Error in parsing.')
        return -1
    
    results = {}
    for i in range(len(generated_guards)):
        generated_guard = generated_guards[i]
        manual_guard = manual_guards[i]
    
        result = generate_sta.check_strength(benchmark, i, generated_guard, manual_guard, parameters, res_cond, snd_vars)
        results[i] = result  

    if all(results[key] == 'unsat' for key in results):
        return 'all'
    elif all(results[key] == 'sat' for key in results):
        return 'none'
    else:
        return 'some'


if __name__ == '__main__':   

    if len(sys.argv) < 3:
        print('Usage: python translateSTA.py $algorithm $check_implication')
        exit()
    alg = str(sys.argv[1])
    check = bool(sys.argv[2])
    
    print('Translating receive STA of {}...'.format(alg))
    snd_file_name = translate_sta(alg)
    print('Tranlation stored in {}'.format(snd_file_name))


    if check:
        result = check_implication(alg)
        if result != -1:
            print('Guard implication: {} of the guards of the generated STA imply the guards of the manual STA'.format(result))
        else:
            print('There was an error in checking the guard implications.')