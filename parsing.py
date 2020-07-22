import importlib

def get_locations(algorithm, package):
    locations = []
    alg = importlib.import_module('.' + algorithm, package = package)
    if alg.local:
        locations = alg.local
    
    return locations

def get_init_locations(algorithm, package):
    init_locations = []
    alg = importlib.import_module('.' + algorithm, package = package)
    if alg.initial:
        init_locations = alg.initial
    
    return init_locations

def get_rules(algorithm, package):
    rules = []
    alg = importlib.import_module('.' + algorithm, package = package)
    if alg.rules:
        rules = alg.rules
    
    return rules

def get_snd_counters(algorithm, package):
    snd_counters = {}
    alg = importlib.import_module('.' + algorithm, package = package)
    if alg.L:
        snd_counters = alg.L.keys()

    return snd_counters

def get_L(algorithm, package):
    L = {}
    alg = importlib.import_module('.' + algorithm, package = package)
    if alg.L:
        L = alg.L

    return L

def get_rcv_counters(algorithm, package):
    rcv_counters = []
    alg = importlib.import_module('.' + algorithm, package = package)
    if alg.rcv_vars:
        rcv_counters = alg.rcv_vars

    return rcv_counters

def get_parameters(algorithm, package):
    parameters = []
    alg = importlib.import_module('.' + algorithm, package = package)
    if alg.params:
        parameters = alg.params
    
    return parameters

def get_resilience_condition(algorithm, package):
    res_cond = []
    alg = importlib.import_module('.' + algorithm, package = package)
    if alg.rc:
        res_cond = alg.rc
    
    return res_cond

def get_phase(algorithm, package):
    phase = 1
    alg = importlib.import_module('.' + algorithm, package = package)
    if alg.phase:
        phase = alg.phase
    
    return phase

def get_environment(algorithm, package):
    environment = []
    alg = importlib.import_module('.' + algorithm, package = package)
    if alg.environment:
        environment = alg.environment
    
    return environment    

def get_constraints(algorithm, package):
    constraints = []
    alg = importlib.import_module('.' + algorithm, package = package)
    if alg.constraints:
        constraints = alg.constraints
    
    return constraints

def get_properties(algorithm, package):
    properties = []
    alg = importlib.import_module('.' + algorithm, package = package)
    if alg.properties:
        properties = alg.properties
    
    return properties