#
# evenBinaryAutomaton.py
#
# HV 2003
#
from scanner import *

# trace FSA dynamics (True | False)
#
#__trace__ = False 
__trace__ = True 

class Automaton(Scanner):

 def __init__(self, stream):
  
  # superclass constructor
  Scanner.__init__(self, stream)

  # define accepting states set
  self.accepting_states=["S2"]

 def __str__(self):
   return str(self.value)

 def transition(self, state, input):
   """
   Encodes transitions and actions
   """

   if state == None:
     # action
     # initialize variables 
     self.value = 0 
     # new state
     return "S1"

   elif state == "S1":
    if   input  == '0':
     # new state
     return "S2"
    elif input  == '1':
     # new state
     return "S3"
    else:
      return None

   elif state == "S2":
    if   input  == '0':
     # new state
     return "S2"
    elif input  == '1':
     # new state
     return "S3"
    else:
      return None

   elif state == "S3":
    if   input  == '0':
     # new state
     return "S2"
    elif input  == '1':
     # new state
     return "S3"
    else:
      return None

   else:
     return None

 def entry(self, state, input):

   if   state == "S2":
     self.value = 2*self.value 
   elif state == "S3":
     self.value = 2*self.value + 1
     
