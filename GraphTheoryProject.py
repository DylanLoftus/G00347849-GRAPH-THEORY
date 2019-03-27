'''
    References : https://web.microsoftstream.com/video/5e2a482a-b1c9-48a3-b183-19eb8362abc9
                 https://web.microsoftstream.com/video/cfc9f4a2-d34f-4cde-afba-063797493a90
                 https://web.microsoftstream.com/video/6b4ba6a4-01b7-4bde-8f85-b4b96abc902a
                 https://swtch.com/~rsc/regexp/regexp1.html
'''

# Dylan Loftus
# Graph Theory Project 2019

# Creating Shunting Yard Algorithm

def shunt(infix):

    # List of special characters and their precedence.
    specials = {'*': 70, '+':60, '?':50, '.': 40, '|': 30}

    # Empty stack
    stack = ""

    # Empty pofix string, will eventually be the infix
    # converted into postfix
    pofix = ""
    
    # For loop loops over the infix string
    for c in infix:
        # If we encounter a ( we add it to the stack.
        if c == '(':
            stack = stack + c
        # If we encounter a ) we take everything off of the stack 
        # and add it to the postfix string.
        elif c == ')':
            while stack[-1] != '(':
                pofix = pofix + stack[-1]
                stack = stack[:-1]
            stack = stack[:-1]
        elif  c in specials:
        # If we encounter a special character. We check the stack to see if there
        # are any other special characters in the stack that have higher precedence
        # than the currently encountered special character. If there is, add it to the
        # postfix string and take it off of the stack. If there is not add it to the stack.
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                pofix = pofix + stack[-1]
                stack = stack[:-1]
            stack = stack + c
        # If we encounter anything else add it to the postfix string.
        else:
            pofix = pofix + c
    # Anything left over in the stack is added to the postfix string.
    while stack:
        pofix = pofix + stack[-1]
        stack = stack[:-1]
    # Returns the compiled infix regular expression
    return pofix

# Class defining a state
class state:
    label = None
    edge1 = None
    edge2 = None

# Class defining a nfa
class nfa:
    initial = None
    accept = None

    # Constructor
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def compile(pofix):
    
    # Array for nfastack.
    nfastack = []

    for c in pofix:
        # If we encounter a '.'
        if c == '.':
            # Pop 2 items off of the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            
            # Join nfa1 accept edge to nfa2's inital state
            nfa1.accept.edge1 = nfa2.initial

            # Append to stack a new nfa with nfa1's initial state and nfa2's accept state.
            nfastack.append(nfa(nfa1.initial, nfa2.accept))
        elif c == '|':
            # Pop 2 items off of the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()

            # Create a state initial
            initial = state()

            # Join inital edge 1 to nfa1's initial state
            initial.edge1 = nfa1.initial
            # Join inital edge 2 to nfa2's initial state
            initial.edge2 = nfa2.initial
            
            # Create a state accept
            accept = state()

            # Join nfa1's accept arrow 1 to the accept state
            nfa1.accept.edge1 = accept
            # Join nfa2's accept arrow 1 to the accept state
            nfa2.accept.edge1 = accept
           
            # Append to stack a new nfa.
            nfastack.append(nfa(initial, accept))
        elif c == '*':
            
            # Pop 1 item off of the stack
            nfa1 = nfastack.pop()
          
            # Create a state initial and accept
            initial = state()
            accept = state()
      
            # Join inital edge 1 to nfa1's initial state
            initial.edge1 = nfa1.initial
            # Join inital edge 2 to accept state
            initial.edge2 = accept

            # Join nfa1's accept edge 1 to nfa1's initial state
            nfa1.accept.edge1 = nfa1.initial
            # Join nfa1's accept edge 2 to the accept state
            nfa1.accept.edge2 = accept

            # Append to stack a new nfa.
            nfastack.append(nfa(initial, accept))
        elif c == '?':
            # Pop 1 item off of the stack
            nfa1 = nfastack.pop()
          
            # Create a state initial and accept
            initial = state()
            accept = state()
      
            # Join inital edge 1 to nfa1's initial state
            initial.edge1 = nfa1.initial
            # Join inital edge 2 to accept state
            initial.edge2 = accept
            # Join nfa1's accept edge 2 to the accept state
            nfa1.accept.edge2 = accept

            # Append to stack a new nfa.
            nfastack.append(nfa(initial, accept))
        elif c == '+':
            # Pop 1 item off of the stack
            nfa1 = nfastack.pop()
          
            # Create a state initial and accept
            initial = state()
            accept = state()
      
            # Join inital edge 1 to nfa1's initial state
            initial.edge1 = nfa1.initial
        
            # Join nfa1's accept edge 1 to nfa1's initial state
            nfa1.accept.edge1 = nfa1.initial
            # Join nfa1's accept edge 2 to the accept state
            nfa1.accept.edge2 = accept

            # Append to stack a new nfa.
            nfastack.append(nfa(initial, accept))
        else:
            # Create a state initial and accept
            accept = state()
            initial = state()
            # Give inital state a label of the character we encountered
            initial.label = c
            # Join initial stage edge 1 to accept
            initial.edge1 = accept

            # Append to stack a new nfa.
            nfastack.append(nfa(initial, accept))

    return nfastack.pop()

def followes(state):

    # Make a new set and add state to it
    states = set()
    states.add(state)

    # Check if the state has any e arrows
    if state.label is None:
        # If the state has an edge 1 follow it
        if state.edge1 is not None:
            states |= followes(state.edge1)
        # If the state has an edge 2 follow it
        if state.edge2 is not None:
            states |= followes(state.edge2)
    # Returns the state and next states that we can get to
    return states

def match(infix, string):
    
    # Change infix reg expression to postfix by calling shunt method
    postfix = shunt(infix)
    # Then compile that postfix reg expression to an nfa
    nfa = compile(postfix)

    # Create current and next set
    current = set()
    nexts = set()

    current |= followes(nfa.initial)

    # Loop through each character in the string
    for s in string:
        # Loop through the states
        for c in current:
            # Checks if the state has the same label as the character we are on
            if c.label == s:
                # Add it to the next set of states and call followes function to get where we can go next by e arrows.
                nexts |= followes(c.edge1)
        # Set the current state as next state and wipe next state for next character 
        current = nexts
        nexts = set()
    # Check if we are in the accept state and return true if yes and false if no
    return (nfa.accept in current)

cont = "y"

# While loop to keep the program running
while cont.casefold() == "y":

    # Ask user for regular expression
    infixes =  input("Enter a regular expression: ")
    # Ask user for string
    strings =  input("Enter a string: ")

    # Print out the result of matching the regular expression to the string
    print(match(infixes, strings),"|",infixes,"|",strings,'|')

    # Ask the user if they want to continue with the program
    cont = input("Continue? Y for yes, N for no: ")




        