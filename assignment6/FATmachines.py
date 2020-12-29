from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class State:
    def __init__(self):
        self.active = False
        self.current = None
        self.total = 0
        self.reassembled = 0

class FATmachine(AtomicDEVS):
    def __init__(self, name):
        AtomicDEVS.__init__(self, name)
        self.in_product = self.addInPort("in_product")
        self.out_product = self.addOutPort("out_product")

    def timeAdvance(self):
        if self.state.active:
            return 0
        else:
            return INFINITY

    def intTransition(self):
        self.state.active = False
        return self.state

    def extTransition(self, inputs):
        self.state.active = True
        self.state.current = inputs[self.in_product]
        return self.state

    def outputFnc(self):
        return {self.out_product: self.state.current}

class Fix(FATmachine):
    def __init__(self):
        FATmachine.__init__(self, "fix")
        self.state = State()

    def extTransition(self, inputs):
        FATmachine.extTransition(self, inputs)
        self.state.current.increaseReas()
        return self.state


class Accept(FATmachine):
    def __init__(self):
        FATmachine.__init__(self, "Accept")
        self.state = State()

    def extTransition(self, inputs):
        FATmachine.extTransition(self, inputs)
        self.state.total += 1
        if inputs[self.in_product].getAmountReas() > 0:
            self.state.reassembled += 1
        return self.state

    def getTotal(self):
        return self.state.total

    def getReassembled(self):
        return self.state.reassembled


class Trash(FATmachine):
    def __init__(self):
        FATmachine.__init__(self, "Trash")
        self.state = State()

    def extTransition(self, inputs):
        FATmachine.extTransition(self, inputs)
        self.state.total += 1
        return self.state

    def getTotal(self):
        return self.state.total


