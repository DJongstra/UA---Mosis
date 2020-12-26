class Item:
    def __init__(self, name=None, creation_time=0.0):
        self.name = name
        self.creation_time = creation_time

class Cube(Item):
    def __init__(self):
        Item.__init__(self, "Cube")

class Cylinder(Item):
    def __init__(self):
        Item.__init__(self, "Cylinder")

class Product(Item):
    def __init__(self, creation_time=0.0):
        Item.__init__(self, "Product", creation_time=creation_time)
        self.times_assembled = 0.0
        self.correctness = 0.0
        self.processing_time = 0.0
