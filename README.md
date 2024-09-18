This is a python project with the purpose of 
simulating different versions of strategy iteration 
in small-scale parity games. There is a number 
of variants, improvement rules, and exponential examples
already implemented, 
and adding your own should be possible. The valuation of 
the strategy improvement algorithm by Jurdziński and Vöge
is assumed (https://doi.org/10.1007/10722167_18)

There is also the option to render images and animations
of runs of strategy iteration. For the improvement rules implemented,
this can be done with a single function call.

The code is not optimized for speed so having large graphs
(more than 100 nodes) or having large exponential examples
with n>=5 may result in long runtimes.

This project uses a custom graph class made by 
Paul Bonsma, Pieter Bos and Tariq Bontekoe

#Prerequisites

This project uses the following packages:

*Generally pre-installed packages:*
os, sys, typing

*Packages from Python library:*
math, tqdm, imageio

*Other:*
graphviz (https://graphviz.org/download/)

#Usage

The main function is run_strategy_iteration_with_counterexample.
It runs some version of strategy iteration on a parity game.
It writes, depending on the settings, the strategies encountered, and makes an animation.

There are some examples of GIF's in the "Example animations" folder

#Inputs

- n: index of the graph G_n
- mode: Version of strategy iteration (default: symmetric or switch-all)
  - mode = 'even' - strategy iteration for player 0/player even 
  - mode = 'odd' - strategy iteration for player 1/player odd 
  - mode = 'symmetric' - symmetric strategy iteration/ improve both player's strategies
- imp_rule: selects improvement rule (default: switch-all)
- counterexample: select which class to take the counterexample from (default: symmetric)
- render: if set to True, render a GIF animation, which is saved as animation.gif. (default: True)
               Additionally, every frame is saved as picture and as gv file in the png/gv folder
- print_iterations: if set to True, write the strategies in every iteration (default: False)
- check_strategy: if True, check if input strategies are valid (default: True)

#Outputs

- G: the graph. one could find the values of nodes in the
        v.valuation0 or v.valuation1 attribute for vertices v of G 
         (depending on type of strategy iteration)
- strat0, strat1: player 0 resp. player 1 optimal strategies

#Improvement rules

The following improvement rules are included:
- "switch-all": switch one edge in every node where there is an improving move
- "symmetric": Symmetric strategy improvement
- "generalizedsymmetric": Relaxation of symmetric strategy improvement
- "othervaluation": Pick edge towards the node where the opponent has the best valuation
- "highestpriority": Switch in the node with the highest priority
- "lowestpriority": Self-explanatory
- "lowestvaluation": Prefer to switch from node with lowest valuation (one-player SI only)
- "highestvaluation": Self-explanatory (one-player SI only)

#Counterexamples

The following parity games with exponential 
running time for their respective improvement 
rule are included:
- "symmetric": for symmetric strategy iteration
- "lessgeneralizedsymmetric": for generalized symmetric strategy iteration
- "generalizedsymmetric": for both generalized SSI and "othervaluation"
- "switchbest": for the switch-best rule (example by Friedmann)
- "highestvaluation": for the "highestvaluation" rule
- "lowestvaluation": what could this be?

#Customization

One could add a new improvement rule as function 
in strategy_iteration.py. Its name should then be added as an
option within select_edges in strategy_iteration.py
One can add a function to create a new parity game class 
in counterexamples.py. The function should then be called
within run_strategy_iteration_with_counterexample in 
strategy_iteration.py. If you want to animate your new parity game, 
it is necessary to specify coordinates for the nodes, initial strategies,
and to specify the variable scalef, which is used to scale
the parity game.
