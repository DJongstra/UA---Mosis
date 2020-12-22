class Product:
    def __init__(self, creationTime):
        self.creationTime = creationTime
        self.processEntryTime = creationTime

    def setEntryTime(self, time):
        self.processEntryTime = time