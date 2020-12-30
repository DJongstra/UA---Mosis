from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY


class OperatorState:
    def __init__(self):
        self.queue = []
        self.currentTime = 0.0
        self.remainingTime = INFINITY
        self.productProcessing = None
        self.totalStatesAssigned = 0


class Operator(AtomicDEVS):
    def __init__(self, name, mean):
        AtomicDEVS.__init__(self, name)
        self.state = OperatorState()
        self.mean = mean

        self.in_product = self.addInPort("in_product")
        self.out_stats = self.addOutPort("out_stats")

    def enterOperator(self, product):
        self.state.remainingTime = self.mean  # calculate time it takes to process this product
        product.setEntryTime(self.state.currentTime)  # set the time the product enters the operator
        self.state.productProcessing = product  # set the product the is currently processed

    def extTransition(self, inputs):
        self.state.currentTime += self.elapsed
        inputs[self.in_product].setQueueTime(self.state.currentTime)     # set queue entry time to current time
        self.state.queue.append(inputs[self.in_product])  # append the product to products to be processed
        if self.state.remainingTime == INFINITY:        # no product currently processed
            self.enterOperator(self.state.queue[0])
        else:
            self.state.remainingTime -= self.elapsed

        return self.state

    def intTransition(self):
        self.state.queue.pop(0)

        if len(self.state.queue) == 0:
            self.state.remainingTime = INFINITY

        else:
            self.enterOperator(self.state.queue[0])

        return self.state

    def timeAdvance(self):
        if self.state.remainingTime < 0:
            return 0
        return self.state.remainingTime


class Assembler(Operator):
    def __init__(self):
        Operator.__init__(self, name="Assembler", mean=4)
        self.out_product = self.addOutPort("out_product")

    def outputFnc(self):
        timeInQueue = self.state.productProcessing.getTimeInQueue()
        return {self.out_product: self.state.productProcessing,
                self.out_stats: timeInQueue}

    def extTransition(self, inputs):
        inputs[self.in_product].setNewCorrectness(self.state.totalStatesAssigned)
        self.state.totalStatesAssigned += 1
        return Operator.extTransition(self, inputs)


class Inspector(Operator):
    def __init__(self, trashPart=0.15, fixPart=0.30):
        Operator.__init__(self, name="Inspector", mean=2)
        self.fixPart = fixPart
        self.trashPart = trashPart
        self.acceptPart = 1 - fixPart - trashPart   # ensuring the three possibilities always add up to one

        self.out_accept = self.addOutPort("out_accept")
        self.out_trash = self.addOutPort("out_trash")
        self.out_fix = self.addOutPort("out_fix")

    def outputFnc(self):
        timeInQueue = self.state.productProcessing.getTimeInQueue()
        correctness = self.state.productProcessing.getCorrectness()
        if correctness < self.trashPart:    # lowest correctness scores are thrashed
            outport = self.out_trash
        elif correctness < (self.trashPart + self.fixPart): # correctness score that are higher than the highest trash score, but lower than the lowest acceptance score are flagged as fixer-uppers
            outport = self.out_fix
        else:
            outport = self.out_accept
        return {outport: self.state.productProcessing,
                self.out_stats: timeInQueue}

