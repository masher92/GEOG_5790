## Project 9 - Cellular automata

A cellular automaton model is based on a grid of cells. The state of the cells is programmed to evolve over a series of time steps 
in accordance with rules defined based on the state of neighbouring cells.

This project creates a cellular automata model of the spread of a forest fire.
It contains two files:
* ca.py : this contains a model of the spread of the forest fire which prints the output to the console.  
* ca_animation.py : this generates a GUI which can be used to initiate a model of the spread of the forst fire which produces an animation of the spread of the fire.   

Current state:
* Animation of the fire spreading is working, but the printing of the fire to the console suggests something not working correctly, e.g. repetition of "ends at iteration 0" statement.

* Additionally, spreading of fire is not even.  It spreads downwards faster than upwards (as within one iteration cells below get set on fire before they are reached)
