from pypdevs.DEVS import AtomicDEVS

class StatisticState:
    def __init__(self):
        self.cylAmount = 0
        self.cubeAmount = 0
        self.currentTime = 0.0
        self.events = []
        self.products = []

class Statistics(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "Statistics")
        self.state = StatisticState()
        self.in_event = self.addInPort("in_event")

    def extTransition(self, inputs):
        self.state.currentTime += self.elapsed
        self.state.events.append(inputs[self.in_event])
        self.state.products.append(inputs[self.in_event])

        return self.state

    def get_time(self):
        return self.state.currentTime

    def get_amount_product(self):
        return len(self.state.products)

    def printEntryProducts(self):
        for prod in self.state.products:
            print(prod.creationTime)
