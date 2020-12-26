from pypdevs.DEVS import AtomicDEVS

# Define the state of the collector as a structured object
class CollectorState(object):
    def __init__(self):
        # Contains received events and simulation time
        self.products = []
        self.current_time = 0.0

class Collector(AtomicDEVS):
    def __init__(self, name=None):
        AtomicDEVS.__init__(self, name)
        self.state = CollectorState()
        self.inport = self.addInPort("input")

    def extTransition(self, inputs):
        self.state.current_time += self.elapsed
        # Calculate time in queue
        print(inputs)
        product = inputs[self.inport]
        time = self.state.current_time - product.creation_time - product.processing_time
        # Add product received
        self.state.products.append(inputs[self.inport])
        return self.state

class Accept(Collector):
    def __init__(self):
        Collector.__init__(self, "Accept")

class Trash(Collector):
    def __init__(self):
        Collector.__init__(self, "Trash")