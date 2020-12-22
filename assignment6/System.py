from pypdevs.DEVS import CoupledDEVS
from ObjectSource import ObjectSource
from Statistics import Statistics
from Preassembler import Preassembler

class Factory(CoupledDEVS):
    def __init__(self):
        CoupledDEVS.__init__(self, "Factory")
        self.cylinder = self.addSubModel(ObjectSource("Cylinder", 3))
        self.cube = self.addSubModel(ObjectSource("Cube", 2))
        self.preassembler = self.addSubModel(Preassembler())
        self.stats = self.addSubModel(Statistics())

        self.connectPorts(self.cylinder.object_out, self.preassembler.in_object)
        self.connectPorts(self.cube.object_out, self.preassembler.in_object)
        self.connectPorts(self.preassembler.out_product, self.stats.in_event)

    def get_cyls(self):
        return self.stats.get_cyls()

    def get_cubes(self):
        return self.stats.get_cubes()

    def get_time(self):
        return self.stats.get_time()