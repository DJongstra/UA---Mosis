from CBDMultipleOutput.Source.CBD import BaseBlock

class ComputerBlock(BaseBlock):
    """
    The negator block will output the value of the input multiplied with -1
    """

    def __init__(self, block_name):
        BaseBlock.__init__(self, block_name, ["IN1"], ["OUT1"])

    def compute(self, curIteration):
        # use this as inspiration for other blocks
        if self.getInputSignal(curIteration, "IN1").value < 10:
            self.appendToSignal(0)
        elif self.getInputSignal(curIteration, "IN1").value < 160:
            self.appendToSignal(10)
        elif self.getInputSignal(curIteration, "IN1").value < 200:
            self.appendToSignal(4)
        elif self.getInputSignal(curIteration, "IN1").value < 260:
            self.appendToSignal(14)
        else:
            self.appendToSignal(6)
