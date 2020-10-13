#import charStream

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


import useCase7Checker

for inp in ["(CL 4) RM 1: Bla Bla Bla ...\n", "(CL 1) RM 1: Bla Bla Bla ...\n", "(CL 5) RM 1: Bla Bla Bla ...\n", "(CL 6) RM 1: Bla Bla Bla ...\n", "(CL 4) RM 5: Bla Bla Bla ...\n", "(CL 4) RM 6: Bla Bla Bla ...\n", "(CL 4) RM 5: Bla Bla Bla ...\ntrek"]:
 str=inp
 sc=useCase7Checker.Automaton(str)
 success=sc.scan()
 if success:
  print(">> recognized "+sc.__str__())
  print(">> committing")
 else:
  print(">> rejected")
  print(">> rolling back")
 print(str)
 print("")