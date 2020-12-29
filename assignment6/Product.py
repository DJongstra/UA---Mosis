from pypdevs.randomGenerator import RandomGenerator


class Product:
    def __init__(self, creationTime):
        self.creationTime = creationTime
        self.processEntryTime = creationTime
        self.processQTime = creationTime
        self.correctness = -1
        self.amountReassembled = 0

    def getCreationTime(self):
        return self.creationTime

    def setEntryTime(self, time):
        self.processEntryTime = time

    def setQueueTime(self, time):
        self.processQTime = time

    def getTimeInQueue(self):
        return self.processEntryTime - self.processQTime

    def getCorrectness(self):
        return self.correctness

    def setNewCorrectness(self, seed=5):
        x = 1
        if self.correctness != -1:
            x = (2 + self.correctness) / 3

        randGen = RandomGenerator(seed)
        self.correctness = randGen.uniform(0, x)

    def getAmountReas(self):
        return self.amountReassembled

    def increaseReas(self):
        self.amountReassembled += 1

