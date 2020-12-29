from pypdevs.DEVS import CoupledDEVS
from ObjectSource import ObjectSource
from Statistics import Statistics
from Preassembler import Preassembler
from Operator import Assembler, Inspector
from FATmachines import Accept, Fix, Trash

class Factory(CoupledDEVS):
    def __init__(self):
        CoupledDEVS.__init__(self, "Factory")
        self.cylinder = self.addSubModel(ObjectSource("Cylinder", 3))
        self.cube = self.addSubModel(ObjectSource("Cube", 2))
        self.preassembler = self.addSubModel(Preassembler())
        self.assembler = self.addSubModel(Assembler())
        self.inspector = self.addSubModel(Inspector())
        self.accept = self.addSubModel(Accept())
        self.fix = self.addSubModel(Fix())
        self.trash = self.addSubModel(Trash())
        self.stats = self.addSubModel(Statistics())

        self.connectPorts(self.cylinder.object_out, self.preassembler.in_object)
        self.connectPorts(self.cube.object_out, self.preassembler.in_object)
        self.connectPorts(self.preassembler.out_product, self.assembler.in_product)
        self.connectPorts(self.assembler.out_stats, self.stats.in_queueTimes)
        self.connectPorts(self.assembler.out_product, self.inspector.in_product)
        self.connectPorts(self.inspector.out_stats, self.stats.in_queueTimes)
        self.connectPorts(self.inspector.out_accept, self.accept.in_product)
        self.connectPorts(self.inspector.out_fix, self.fix.in_product)
        self.connectPorts(self.fix.out_product, self.assembler.in_product)
        self.connectPorts(self.inspector.out_trash, self.trash.in_product)

        self.connectPorts(self.accept.out_product, self.stats.in_product)
        self.connectPorts(self.trash.out_product, self.stats.in_product)

    def printStatistics(self, filename):
        file = open(filename, "w")

        totalProducts = self.stats.getTotalProducts()
        file.write("Total number of created products: " + str(totalProducts))
        file.write("\nAmount of reassemblies for any product:")
        reas = self.stats.getReassemblies()
        for key, value in sorted(reas.items()):
            file.write("\n  -> " + str(key) + " reassemblies - " + str(value) + " times")

        file.write("\nPercentage in trash:\n   " + str(self.trash.getTotal()/totalProducts * 100) + " %\n")
        file.write("Percentage accepted:\n   " + str(self.accept.getTotal()/totalProducts * 100) + " %\n")
        file.write("Percentage of Accepted reassembled:\n   " + str(self.accept.getReassembled() / self.accept.getTotal() * 100) + " %\n")

        file.write("Average queue time:\n   " + str(self.stats.getAverageWaitingTime()) + " minutes\n")
        file.write("Average time in system:\n   " + str(self.stats.getAverageTotalTime()) + " minutes\n")

        file.close()


