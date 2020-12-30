from pypdevs.simulator import Simulator

from System import Factory

model = Factory()
simulator = Simulator(model)

simulator.setVerbose("SimulationOutput.txt")
simulator.setClassicDEVS()
simulator.setTerminationTime(26.0)
simulator.simulate()

simulator.model.printStatistics("./statsDeterministic.txt")
