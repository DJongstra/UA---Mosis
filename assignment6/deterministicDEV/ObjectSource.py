from pypdevs.DEVS import AtomicDEVS, CoupledDEVS

class ObjectSource(AtomicDEVS):
    def __init__(self, name, time):
        AtomicDEVS.__init__(self, name)
        self.time = time

        self.object_out = self.addOutPort(name="object_out")

    def timeAdvance(self):
        return self.time

    def outputFnc(self):
        # Output the new event on the output port
        return {self.object_out: self.getModelName()}

