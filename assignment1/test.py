#import charStream

print(">> testing binary string recognition/accepance of even number")

import useCase3Checker

for inp in ["(CR 0) AC 4.\n(CL 4) AB 0.\n", "(CR 0) AC 4.\n(CL 4) AB 0.", "(CR 0) AC 4.\n(CL 0) AB 4.\n", "(CR 0) AC 0.\n(CL 0) AB 0.\n"]:
 str=inp
 sc=useCase3Checker.Automaton(str)
 success=sc.scan()
 if success:
  print(">> recognized "+sc.__str__())
  print(">> committing")
 else:
  print(">> rejected")
  print(">> rolling back")
 print(str)
 print("")
