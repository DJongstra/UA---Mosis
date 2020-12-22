from pypdevs.DEVS import AtomicDEVS
from Product import Product
from pypdevs.infinity import INFINITY

class PreassemblerState():
    def __init__(self):
        self.cylinders = 0
        self.cubes = 0
        self.time = 0.0


class Preassembler(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "Preassembler")
        self.state = PreassemblerState()

        self.in_object = self.addInPort("in_object")
        self.out_product = self.addOutPort("out_product")

    def intTransition(self):
        self.state.cubes -= 2
        self.state.cylinders -= 1
        return self.state

    def extTransition(self, inputs):
        self.state.time += self.elapsed

        if inputs[self.in_object] == "Cylinder":
            self.state.cylinders += 1

        elif inputs[self.in_object] == "Cube":
            self.state.cubes += 1

        return self.state

    def timeAdvance(self):
        if self.state.cylinders >= 1 and self.state.cubes >= 2:
            return 0
        else:
            return INFINITY


    def outputFnc(self):
        return {self.out_product: Product(self.state.time)}

