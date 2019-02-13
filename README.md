# syncTA

Encodings of synchronous fault-tolerant distributed algorithms as synchronous threshold automata. 

We verify safety of these algorithms using bounded model checking, that is, by encoding safety violations as reachability queries on bounded executions. Using two SMT-based procedures, we first find the bound on the length of the executions we consider, and then check reachability of a bad state.

<h4>Prerequisites</h4>
We currently support the SMT solvers <a href="https://github.com/Z3Prover/z3">Z3</a> and <a href="https://github.com/CVC4/CVC4">CVC4</a>.
To be able to run our scripts, make sure you have Python, Z3 and CVC4 installed, and on your $PATH. 

<h3>Contents</h3>
There are three packages:
<ul>
  <li><code>algorithms</code>, containing the algorithms for which we compute the diameter using SMT</li>
  <li><code>boundable</code>, containing the algorithms for which additionally we have a theoretical bound on the diameter</li>
  <li><code>conuterexamples</code>, containing erroneous encodings of the algorithms</li>
</ul>  

<h3>Running the experiments</h3>
You can check the safety of the encoded algorithms by 
<code>
$ python run.py solver
</code>

You can check the safety of the algorithms for which we have a theoretical bound on the diameter by
<code>
$ python run_boundable.py solver
</code>

You can check that the erroneous versions contain counterexamples by 
<code>
$ python run_counterexamples.py solver
</code>

In all cases, <code>solver</code> is either <code>z3</code> or <code>cvc4</code>.
