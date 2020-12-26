import numpy as np
from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

from assignment.Item import Product


class MachineState:
    def __init__(self):
        self.processing_time = INFINITY
        self.product = None


class Machine(AtomicDEVS):
    def __init__(self, name=None):
        AtomicDEVS.__init__(self, name)
        self.state = MachineState()
        self.inport = self.addInPort("input")
        self.outport = self.addOutPort("output")

    def timeAdvance(self):
        return self.state.processing_time

    def outputFnc(self):
        return {self.outport: self.state.product}

    def extTransition(self, inputs):
        self.state.product = inputs[self.inport]
        return self.state

    def intTransition(self):
        self.state.product = None
        return self.state


class PreassemblerState(MachineState):
    def __init__(self):
        MachineState.__init__(self)
        self.cubes_in_queue = []
        self.cylinders_in_queue = []


class Preassembler(Machine):
    def __init__(self):
        Machine.__init__(self, "Preassembler")
        self.inport2 = self.addInPort("input2")
        self.state = PreassemblerState()

    # def intTransition(self):
    #     print(len(self.state.cubes_in_queue))
    #     print(len(self.state.cylinders_in_queue))
    #     return self.state

    def extTransition(self, inputs):
        if self.inport in inputs:
            self.state.cylinders_in_queue.append(inputs[self.inport])
        if self.inport2 in inputs:
            self.state.cubes_in_queue.append(inputs[self.inport2])

        if len(self.state.cubes_in_queue) > 2 and len(self.state.cylinders_in_queue) > 0:
            self.state.cylinders_in_queue.pop()
            self.state.cubes_in_queue.pop()
            self.state.cubes_in_queue.pop()
            self.state.product = Product()
            self.state.processing_time = 1.0
        else:
            self.state.processing_time = INFINITY
        return self.state


class ProcessorState(MachineState):
    def __init__(self, processing_mu, processing_sigma=1.0):  # mean and standard deviation
        MachineState.__init__(self)
        self.products_in_queue = []
        self.current_time = 0.0
        self.processing_mu = processing_mu
        self.processing_sigma = processing_sigma


class Processor(Machine):
    def __init__(self, name="Processor"):
        Machine.__init__(self, name)
        self.state = ProcessorState(processing_mu=1.0)

    def calculate_processing_time(self):
        random_time_sample = np.random.normal(self.state.processing_mu, self.state.processing_sigma, 1)
        self.state.processing_time = random_time_sample[0]


class Assembler(Processor):
    def __init__(self):
        Processor.__init__(self, "Assembler")
        self.state = ProcessorState(processing_mu=4.0)

    def intTransition(self):
        # If we have an item in the queue
        # Pop it and work on it
        if len(self.state.products_in_queue) > 0:
            #  get product
            self.state.product = self.state.products_in_queue.pop()
            #  add time
            self.calculate_processing_time()
            self.state.current_time += self.timeAdvance()
            self.state.product.creation_time = self.state.current_time
            # add correctness
            self.state.product.correctness = self.calculate_correctness()
        else:
            self.state.product = None
            self.state.processing_time = INFINITY
        return self.state

    def extTransition(self, inputs):
        self.state.products_in_queue.append(inputs[self.inport])
        return self.state

    def calculate_correctness(self):
        random_correctness_sample = []
        if self.state.product.times_assembled == 0.0:
            random_correctness_sample = np.random.uniform(0, 1.0, 1)
        elif self.state.product.times_assembled > 0.0:
            c = self.state.product.correctness
            limit = (2 + c) / 3
            random_correctness_sample = np.random.uniform(0, limit, 1)
        return random_correctness_sample[0]




class Inspector(Processor):
    def __init__(self):
        Processor.__init__(self, "Inspector")
        self.state = ProcessorState(processing_mu=2.0)
        self.outport2 = self.addOutPort("output2")
        self.outport3 = self.addOutPort("output3")

    def intTransition(self):
        # If we have an item in the queue
        # Pop it and work on it
        if len(self.state.products_in_queue) > 0:
            #  get product
            self.state.product = self.state.products_in_queue.pop()
            # add time
            self.calculate_processing_time()
            self.state.product.processing_time += self.timeAdvance()
        else:
            self.state.product = None
            self.state.processing_time = INFINITY
        return self.state

    def extTransition(self, inputs):
        self.state.products_in_queue.append(inputs[self.inport])
        return self.state

    def outputFnc(self):
        # choose destination based on correctness of product
        # outport => accept = correctness > 0.45
        # outport2 => fix = 0.15 < correctness < 0.45
        # outport3 => trash = else
        port = self.outport
        if self.state.product:
            if self.state.product.correctness > 0.45:
                port = self.outport
            elif 0.15 < self.state.product.correctness < 0.45:
                port = self.outport2
            else:
                port = self.outport3
        return {port: self.state.product}


class Fix(Machine):
    def __init__(self):
        Machine.__init__(self, "Fix")
        self.state = MachineState()
        print(self.state)

    def extTransition(self, inputs):
        self.state.product = inputs[self.inport]
        # If we have an item in the queue
        # Pop it and work on it
        if self.state.product:
            self.state.processing_time = 0.0
        else:
            self.state.processing_time = INFINITY
        return self.state