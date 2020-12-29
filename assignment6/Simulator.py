from pypdevs.simulator import Simulator

from System import Factory

model = Factory(fixPart=0.20, trashPart=0.10)
simulator = Simulator(model)

simulator.setVerbose("SimulationOutput.txt")
simulator.setClassicDEVS()
simulator.setTerminationTime(2000.0)
simulator.simulate()

simulator.model.printStatistics("./statsOtherInspector.txt")
