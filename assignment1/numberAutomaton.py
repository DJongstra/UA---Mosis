#
# numberAutomaton.py
#
# HV 2003
#

from scanner import *

## see http://msdl.cs.mcgill.ca/people/hv/teaching/SoftwareDesign/COMP304B2003/assignments/assignment3/solution/
##
class Automaton(Scanner):

 def __init__(self, stream):
  
   # superclass constructor
   Scanner.__init__(self, stream)

   # define accepting states
   self.accepting_states=["S2","S4","S7"]

 def __str__(self):
  
   return str(self.value)+"E"+str(self.exp)


 def transition(self, state, input):
   """
   Encodes transitions and actions
   """

   if state == None:
      # action
      # initialize variables 
      self.value = 0 
      self.exp = 0
      # new state
      return "S1"

   elif state == "S1":
    if input  == '.':
      # action
      self.scale = 0.1
      # new state
      return "S3"
    elif '0' <= input <= '9':
      # action
      self.value = ord(input.lower())-ord('0')
      # new state
      return "S2"
    else:
      return None

   elif state == "S2":
    if input  == '.':
      # action
      self.scale = 0.1
      # new state
      return "S4"
    elif '0' <= input <= '9':
      # action
      self.value = self.value*10+ord(input.lower())-ord('0')
      # new state
      return "S2"
    elif input.lower()  == 'e':
      # action
      self.exp = 1
      # new state
      return "S5"
    else:
      return None

   elif state == "S3":
    if '0' <= input <= '9':
      # action
      self.value += self.scale*(ord(input.lower())-ord('0'))
      self.scale /= 10
      # new state
      return "S4"
    else:
      return None

   elif state == "S4":
    if '0' <= input <= '9':
      # action
      self.value += self.scale*(ord(input.lower())-ord('0'))
      self.scale /= 10
      # new state
      return "S4"
    elif input.lower()  == 'e':
      # action
      self.exp = 1
      # new state
      return "S5"
    else:
      return None

   elif state == "S5":
    if   input  == '+':
      # new state
      return "S6"
    elif input  == '-':
      # action
      self.exp = -1
      # new state
      return "S6"
    elif '0' <= input <= '9':
      # action
      self.exp *= ord(input.lower())-ord('0')
      # new state
      return "S7"
    else:
      return None

   elif state == "S6":
    if '0' <= input <= '9':
      # action
      self.exp *= ord(input.lower())-ord('0')
      # new state
      return "S7"
    else:
      return None

   elif state == "S7":
    if '0' <= input <= '9':
      # action
      self.exp = self.exp*10+ord(input.lower())-ord('0')
      # new state
      return "S7"
    else:
      return None

   else:
    return None

 def entry(self, state, input):

   pass

