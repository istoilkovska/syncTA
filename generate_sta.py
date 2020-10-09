import helper
import os

def translate_rules(algorithm, rcv_rules, parameters, rc, rcv_vars, snd_vars, rcv_environment):
    """
    Given the rules of a receiveTA, return a list of rules of the sendTA
    """
    rcv_guards = [r['guard'] for r in rcv_rules]
    sta_guards = generate_sta_guards(algorithm, rcv_guards, parameters, rc, rcv_vars, snd_vars, rcv_environment)

    return [{'idx' : r['idx'],
             'from' : r['from'],
             'to' : r['to'],
             'guard' : sta_guards[r['idx']]} for r in rcv_rules]

def generate_sta_guards(algorithm, rcv_guards, parameters, rc, rcv_vars, snd_vars, rcv_environment):

    sta_guards = []

    for idx, rcv_guard in enumerate(rcv_guards):
        if all(rcv_guard.find(rcv_v) == -1 for rcv_v in rcv_vars):
            sta_guards.append(rcv_guard)

        else:
            q_guard = rcv_to_quantified_guard(rcv_guard, rcv_vars, rcv_environment)
            q_file = write_quantified_guard_to_smt_file(algorithm, idx, q_guard, parameters, rc, snd_vars)
            err, qe_output = helper.call_solver('z3', q_file, 300)

            if err == 0: 
                sta_guard = qe_output_to_guard(qe_output)
            else:
                sta_guard = 'false'
                print('Guard nr. {} could not be translated.'.format(idx))
                print('The smt solver reported the following output:\n')
                print(qe_output)

            sta_guards.append(sta_guard)

    return sta_guards

def rcv_to_quantified_guard(rcv_guard, rcv_vars, rcv_environment):
    """
    Translate a receive guard to an smt guard, where the receive guard is 
    strengthened by rcv_environment, and the receive variables are existentially quantified
    """
    strong_guard = '(and\n{}\n{})'.format(rcv_guard, '\n'.join(rcv_environment))
    smt_ex_vars = ' '.join(['({} Int)'.format(rcv_v) for rcv_v in rcv_vars])
    smt_formula = '(exists ({})\n{}\n)'.format(smt_ex_vars, strong_guard)

    return smt_formula

def write_quantified_guard_to_smt_file(algorithm, idx, smt_formula, parameters, rc, snd_vars):
    intro = '{}{}'.format('(set-option :pp.max_depth 100)\n', helper.introduction(parameters, rc, 'z3'))

    snd_vars_declaration = ['(declare-const {} Int)'.format(s) for s in snd_vars]
    snd_constraints = ['(>= {} 0)'.format(s) for s in snd_vars]

    outro = '(apply (then simplify qe-light qe2 ctx-solver-simplify (using-params simplify :arith_ineq_lhs true)))'

    file_dir = os.path.dirname(os.path.realpath('__file__'))
    tmp_subdir = os.path.join(file_dir, 'tmp')

    if not os.path.isdir(tmp_subdir):
        os.makedirs(tmp_subdir)

    tmp_file_name = os.path.join(tmp_subdir, 'qe-{}-{}.smt'.format(algorithm, idx))
    
    tmp_file = open(tmp_file_name, 'w')
    tmp_file.write(intro)
    tmp_file.write('\n\n')
    tmp_file.write('\n'.join(snd_vars_declaration))
    # tmp_file.write('\n\n')
    # tmp_file.write('(assert\n(and\n{})\n)'.format('\n'.join(snd_constraints)))
    tmp_file.write('\n\n')
    tmp_file.write('(assert\n{})\n'.format(smt_formula))
    tmp_file.write('\n\n')
    tmp_file.write(outro)
    tmp_file.close()

    return tmp_file_name   


def qe_output_to_guard(smt_output):
    eliminated = smt_output.split('\n')[2:-2]
    return '(and {})'.format(' '.join([e.strip() for e in eliminated]))

def write_sndta(snd_file_name, locations, L, init_locations, rules, parameters, res_cond, constraints, phase, properties):
    snd_file = open(snd_file_name, 'w')
    
    snd_file.write('# process local states\n')
    snd_file.write('local = {}\n\n'.format(locations))
    
    snd_file.write('# L states\n')
    snd_file.write('L = {}\n\n'.format(L))

    snd_file.write('# initial states \n')
    snd_file.write('initial = {}\n\n'.format(init_locations))
    
    snd_file.write('# rules\n')
    snd_file.write('rules = {}\n\n'.format(rules))

    snd_file.write('# process local states\n')
    snd_file.write('local = {}\n\n'.format(locations))
    
    snd_file.write('# parameters, resilience condition\n')
    snd_file.write('params = {}\n\n'.format(parameters))
    snd_file.write('rc = {}\n\n'.format(res_cond))

    snd_file.write('# phase\n')
    snd_file.write('phase = {}\n\n'.format(phase))


    snd_file.write('# configuration/transition constraints\n')
    snd_file.write('constraints = {}\n\n'.format(constraints))

    snd_file.write('# safety properties\n')
    snd_file.write('properties = {}\n\n'.format(properties))

    snd_file.close()

    
def check_strength(benchmark, idx, generated_guard, manual_guard, parameters, res_cond, snd_vars):

    file_dir = os.path.dirname(os.path.realpath('__file__'))
    tmp_subdir = os.path.join(file_dir, 'tmp')

    if not os.path.isdir(tmp_subdir):
        os.makedirs(tmp_subdir)

    smt_file_name = os.path.join(tmp_subdir, 'guard-impl-{}-{}.smt'.format(benchmark, idx))

    snd_vars_declaration = ['(declare-const {} Int)'.format(s) for s in snd_vars]
    snd_constraints = ['(>= {} 0)'.format(s) for s in snd_vars]

    smt_file = open(smt_file_name, 'w')

    smt_file.write(helper.introduction(parameters, res_cond, 'z3'))
    smt_file.write('\n\n')
    smt_file.write('\n'.join(snd_vars_declaration))
    smt_file.write('\n\n')
    smt_file.write('(assert\n(and\n{})\n)'.format('\n'.join(snd_constraints)))
    smt_file.write('\n\n')
    smt_file.write('(assert\n(and\n{}\n(not\n{})))'.format(generated_guard, manual_guard))
    smt_file.write('(check-sat)')
    smt_file.close()

    err, impl_output = helper.call_solver('z3', smt_file_name, 300)

    if err == 0: 
        return impl_output
    else:
        return 'false'
    
