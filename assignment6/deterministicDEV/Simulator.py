from pypdevs.simulator import Simulator

from System import Factory

model = Factory()
simulator = Simulator(model)

simulator.setVerbose("SimulationOutput.txt")
simulator.setClassicDEVS()
simulator.setTerminationTime(62.0)
simulator.simulate()

simulator.model.printStatistics("./statsDeterministic62m.txt")
