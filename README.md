# Algorithms and Complexity: 2-Way Deterministic Finite Automata

Run 'gui.py' to start the program.

This program uses Tkinter as the GUI library. 

The program will initialize the machine defined in 'sample.txt'.
It will have an initial input string "aaabb".

Button Controls:
-
- Run &rarr; runs the input string through the machine with the given definition until an accept or reject verdict is reached

- Step &rarr; feeds the input string through the machine step by step (reading one input symbol every click)

- Reset &rarr; resets the whole machine, also used to change the input string.

Change Input: Enter input string in text field &rarr; Reset

Machine Definition:
-
To change machine definition, open the .txt file of your choosing.
The machine definition file format is as follows and can also be seen in 'sample.txt':

&rarr; Each line is a python tuple defining a state: label (string), transitions (tuple list), final state (boolean)

&rarr; Final states, accepting or rejecting, should have a 'True' value.

&rarr; Reject states should be labeled with the first character being 'r' (e.g. r, r1).

&rarr; Transitions are defined as tuples in the following format: ('input_character', 'direction', 'state')

Where:
- input_character: Represents the input symbol that triggers the transition.
- direction: Specifies the direction of movement after processing the input symbol.
- state: Indicates the new state the system will transition to after processing the input symbol.

&rarr; Directions are {'L', 'S', 'R'} for left, still, and right respectively.

&rarr; First state defined will always be initial state.

&rarr; Endmarkers are {'<','>'} for the left and right ends.

Sample Line &rarr;  ('q0', [('<','R','q1'),('0','R','q1'),('1','L','q0'),('>','L','q0')], False)
