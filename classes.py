
"""this is the machine give it a list of State objects. the element is always the start state

    members:
        list: states is a list of State objects
        run: is the current state. the first state is always the first object in states
        
"""
class Machine:
    def __init__(self, states):
        if not states:
            raise ValueError("No states provided. The states list must not be empty.")
        self.states = states
        self.run = self.states[0]
        """this function lets machine read the character. 
        returns: a tuple of (new current state, read direction)
        """
    def read_char(self, char):
        try:
            delta = self.run.get_delta(char)
        except StopIteration:
             raise ValueError("Invalid transition passed in State: " + self.run.label)
         
        print(f"Delta: {delta}")
        _, direction, next_state_label = delta
        next_state = next((state for state in self.states if state.label == next_state_label), None)
        if next_state is None:
            raise ValueError("State " + next_state_label + " is unreachable")
        self.run = next_state
        return (self.run, direction)

    def isFinal(self):
        return self.run.isFinal         
    
    def reset(self):
        self.run = self.states[0]

        """This class simulates a state in a machine

        members:
            string: label is the label of state
            list: delta contains a list of tuples that represent the transitions
            boolean: isFinal dictates if it is a final state
        notes:
            the list members are of the following types:
                (string_literal, Number,string_literal)
                they stand for (next state label, direction of read (-1 for left, 0 for stay, 1 for right), the character to read)
        """
class State:
    def __init__(self,state):
        self.label, self.delta, self.isFinal = state
        """find a valid transition given character
        """
    def get_delta(self,char):

            delta = next(val for val in self.delta if val[0] == char)
            return delta
