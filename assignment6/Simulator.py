from pypdevs.simulator import Simulator

from System import Factory

model = Factory()
simulator = Simulator(model)

simulator.setVerbose()
simulator.setClassicDEVS()
simulator.setTerminationTime(32.0)
simulator.simulate()

print(model.stats.get_amount_product())
print(model.stats.get_time())
print(model.stats.printEntryProducts())
