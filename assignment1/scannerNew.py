### !!Scanner is edited because there was not an import charStream and I couldn't find anywhere how to install it


#
# scanner.py
#
# HV 2003
#
import string

# trace FSA dynamics (True | False)
#__trace__ = False 
__trace__ = True 

class Scanner:
 """
  A simple Finite State Automaton simulator.
  Used for scanning an input stream.
 """
 def __init__(self, stream):
  self.set_stream(stream)
  self.pos = -1
  self.current_state=None
  self.accepting_states=[]

 def set_stream(self, stream):
  self.stream = stream

 def scan(self):

  self.current_state=self.transition(self.current_state, None)

  if __trace__:
    print("\ndefault transition --> "+self.current_state)

  while 1:
    # look ahead at the next character in the input stream
    self.pos += 1
    if self.pos >= len(self.stream): break
    next_char = self.stream[self.pos]


    # stop if this is the end of the input stream


    if __trace__:
      print(str(self.stream))
      if self.current_state != None:
        print("transition "+self.current_state+" -|"+next_char, end = '')
   
    # perform transition and its action to the appropriate new state 
    next_state = self.transition(self.current_state, next_char)

    if __trace__:
      if next_state == None: 
        print()
      else:
        print("|-> "+next_state)
    

    # stop if a transition was not possible
    if next_state == None: 
      break
    else:
      self.current_state = next_state
      # perform the new state's entry action (if any)
      self.entry(self.current_state, next_char)

    # now, actually consume the next character in the input stream
    next_char = self.stream[self.pos]

  if __trace__:
    print(str(self.stream)+"\n")

  # now check whether to accept consumed characters
  success = self.current_state in self.accepting_states
  if success:
    return success
  else:
   pass
  return success

