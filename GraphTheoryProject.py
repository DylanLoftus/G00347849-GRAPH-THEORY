# Dylan Loftus
# Graph Theory Project 2019

# Creating Shunting Yard Algorithm

def shunt(infix):

    # List of special characters and their precedence.
    specials = {'*': 50, '.': 40, '|': 30}

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
        if c == '.':
           
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            
            nfa1.accept.edge1 = nfa2.initial
           
            nfastack.append(nfa(nfa1.initial, nfa2.accept))
        elif c == '|':
            
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
          
            initial = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            
            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
           
            nfastack.append(nfa(initial, accept))
        elif c == '*':
            
            nfa1 = nfastack.pop()
          
            initial = state()
            accept = state()
      
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
   
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
     
            nfastack.append(nfa(initial, accept))
        else:
   
            accept = state()
            initial = state()

            initial.label = c
            initial.edge1 = accept

            nfastack.append(nfa(initial, accept))

    return nfastack.pop()

def followes(state):

    states = set()
    states.add(state)

    if state.label is None:
        if state.edge1 is not None:
            states |= followes(state.edge1)
      
        if state.edge2 is not None:
            states |= followes(state.edge2)

    return states

def match(infix, string):

    postfix = shunt(infix)
    nfa = compile(postfix)

  
    current = set()
    nexts = set()

    current |= followes(nfa.initial)

    for s in string:
        for c in current:
            if c.label == s:
                nexts |= followes(c.edge1)

        current = nexts
        nexts = set()

    return (nfa.accept in current)


infixes = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c"]
strings = ["", "abc", "abbc", "abcc", "abad", "abbbc"]

for i in infixes:
    for s in strings:
        print(match(i, s), i , s)