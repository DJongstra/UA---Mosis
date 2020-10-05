import charStream

print(">> testing binary string recognition/accepance of even number")

import evenBinaryAutomaton

for inp in ["", "0001", "0101", "11111"]:
 str=charStream.CharacterStream(inp)
 sc=evenBinaryAutomaton.Automaton(str)
 success=sc.scan()
 if success:
  print(">> recognized "+sc.__str__())
  print(">> committing")
  str.commit()
 else: 
  print(">> rejected")
  print(">> rolling back")
  str.rollback()
 print(str)
 print("")


print(">> testing floating point number recognition/computation of value")

import numberAutomaton

for inp in [".", "12", "12.3e+1", "12.3e1", "e3", "10ab",\
            "10e3", "10E-3", ".10", ".10e3", "10.", "10.3e44"]:
 str=charStream.CharacterStream(inp)
 sc=numberAutomaton.Automaton(str)
 success=sc.scan()
 if success:
  print(">> recognized "+sc.__str__())
  print(">> committing")
  str.commit()
 else: 
  print(">> rejected")
  print(">> rolling back")
  str.rollback()
 print(str)
 print("")

