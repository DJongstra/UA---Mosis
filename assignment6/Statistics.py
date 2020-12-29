from pypdevs.DEVS import AtomicDEVS
from statistics import mean


class StatisticState:
    def __init__(self):
        self.currentTime = 0.0
        self.waitingTimes = []
        self.totalProducts = 0
        self.amountReassembled = dict()
        self.totalTimes = []


class Statistics(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "Statistics")
        self.state = StatisticState()
        self.in_queueTimes = self.addInPort("in_queueTimes")
        self.in_product = self.addInPort("in_product")

    def extTransition(self, inputs):
        self.state.currentTime += self.elapsed
        if self.in_queueTimes in inputs:
            self.state.waitingTimes.append(inputs[self.in_queueTimes])

        if self.in_product in inputs:
            product = inputs[self.in_product]
            self.state.totalProducts += 1
            self.state.totalTimes.append(self.state.currentTime - product.getCreationTime())
            reassembled = product.getAmountReas()
            if reassembled in self.state.amountReassembled:
                self.state.amountReassembled[reassembled] += 1
            else:
                self.state.amountReassembled[reassembled] = 1

        return self.state

    def getTime(self):
        return self.state.currentTime

    def getAverageWaitingTime(self):
        return mean(self.state.waitingTimes)

    def getTotalProducts(self):
        return self.state.totalProducts

    def getReassemblies(self):
        return self.state.amountReassembled

    def getAverageTotalTime(self):
        return mean(self.state.totalTimes)


