from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

from assignment.Item import Cube, Cylinder, Item

class SourceState:
    def __init__(self, seed, processing_time):
        self.current_time = 0.0
        self.processing_time = processing_time
        self.seed = seed

class Source(AtomicDEVS):
    def __init__(self, name=None, seed=1.0, processing_time=1.0):
        AtomicDEVS.__init__(self, name)
        self.state = SourceState(seed, processing_time)
        self.outport = self.addOutPort("output")

    def timeAdvance(self):
        return self.state.processing_time

    def outputFnc(self):
        actual_creation_time = self.state.current_time + self.state.processing_time
        return {self.outport: Item(creation_time=actual_creation_time)}

    def intTransition(self):
        self.state.current_time += self.timeAdvance()
        self.state.seed -= 1
        if self.state.seed == 0:
            self.state.processing_time = INFINITY
        return self.state

class CubeSource(Source):
    def __init__(self, seed=1.0):
        Source.__init__(self, "CubeSource", seed, 2.0)

    def outputFnc(self):
        return {self.outport: Cube()}

class CylinderSource(Source):
    def __init__(self, seed=1.0):
        Source.__init__(self, "CylinderSource", seed, 3.0)

    def outputFnc(self):
        return {self.outport: Cylinder()}