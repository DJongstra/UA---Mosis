from pypdevs.DEVS import CoupledDEVS
from pypdevs.simulator import Simulator

from factory.Collector import Accept, Trash
from factory.Machine import Preassembler, Assembler, Inspector, Fix
from factory.Source import CylinderSource, CubeSource


class Factory(CoupledDEVS):
    def __init__(self):
        CoupledDEVS.__init__(self, "Factory")
        self.cylinder_source = self.addSubModel(CylinderSource(seed=10.0))
        self.cube_source = self.addSubModel(CubeSource(seed=20.0))
        self.preassembler = self.addSubModel(Preassembler())
        self.assembler = self.addSubModel(Assembler())
        self.inspector = self.addSubModel(Inspector())
        self.fix = self.addSubModel(Fix())
        self.accept = self.addSubModel(Accept())
        self.trash = self.addSubModel(Trash())


        self.connectPorts(self.cylinder_source.outport, self.preassembler.inport)
        self.connectPorts(self.cube_source.outport, self.preassembler.inport2)
        self.connectPorts(self.preassembler.outport, self.assembler.inport)
        self.connectPorts(self.assembler.outport, self.inspector.inport)
        self.connectPorts(self.inspector.outport, self.accept.inport)
        self.connectPorts(self.inspector.outport2, self.fix.inport)
        self.connectPorts(self.inspector.outport3, self.trash.inport)
        self.connectPorts(self.fix.outport, self.assembler.inport)

if __name__ == '__main__':
    model = Factory()
    sim = Simulator(model)
    # sim.setVerbose(None)
    sim.setVerbose("myOutputFile")
    # Required to set Classic DEVS, as we simulate in Parallel DEVS otherwise
    sim.setClassicDEVS()
    sim.simulate()
    print(model.accept.state.products)
    print(model.trash.state.products)