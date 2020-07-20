# syncTA

Encodings of synchronous fault-tolerant distributed algorithms as synchronous threshold automata. 

We verify safety of these algorithms using bounded model checking, that is, by encoding safety violations as reachability queries on bounded executions. Using two SMT-based procedures, we first find the bound on the length of the executions we consider, and then check reachability of a bad state.

### Prerequisites
We currently support the SMT solvers [Z3](https://github.com/Z3Prover/z3) and [CVC4](https://github.com/CVC4/CVC4).
To be able to run our scripts, make sure you have Python, Z3 and CVC4 installed, and on your `$PATH`. 

### Contents
There are three packages:
- `algorithms`, containing the algorithms for which we compute the diameter using SMT
- `boundable`, containing the algorithms for which additionally we have a theoretical bound on the diameter
- `conuterexamples`, containing erroneous encodings of the algorithms

## Running the experiments
You can check the safety of the encoded algorithms by 
```bash
$ python run.py solver
```

You can check the safety of the algorithms for which we have a theoretical bound on the diameter by
```bash
$ python run_boundable.py solver
```

You can check that the erroneous versions contain counterexamples by 
```bash
$ python run_counterexamples.py solver
```

In all cases, `solver` is either `z3` or `cvc4`.
