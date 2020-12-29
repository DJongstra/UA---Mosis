assigningList = [1, 1, 0.4, 1, 1, 0, 0.4, 1, 1, 0.4, 1, 0, 0.4, 1, 1, 0.4, 1, 0, 0.4, 1]

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

    def setNewCorrectness(self, nrAssigning):
        nrAssigning = nrAssigning % 20
        self.correctness = assigningList[nrAssigning]

    def getAmountReas(self):
        return self.amountReassembled

    def increaseReas(self):
        self.amountReassembled += 1

