from pypdevs.simulator import Simulator

from System import Factory

model = Factory()
simulator = Simulator(model)

simulator.setVerbose("SimulationOutput.txt")
simulator.setClassicDEVS()
<<<<<<< HEAD:assignment6/AAAtemp/Simulator.py
simulator.setTerminationTime(54.0)
=======
simulator.setTerminationTime(2000)
>>>>>>> 86a887ee67d6c83582053a53f37fe8c64ac9ba9b:assignment6/deterministicDEV/Simulator.py
simulator.simulate()

simulator.model.printStatistics("./statsDeterministic3.txt")
