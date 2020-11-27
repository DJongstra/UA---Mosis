from CBDMultipleOutput.Source.CBD import BaseBlock


class ComputerBlock(BaseBlock):

    """
    The combuter block implements a predefined trajectory over time
    """

    def __init__(self, block_name):
        BaseBlock.__init__(self, block_name, ["IN1"], ["OUT1"])

    def compute(self, curIteration):
        input_time = self.getInputSignal(curIteration, "IN1").value
        output = 0
        if input_time >= 10 and input_time < 160:
            output = 10
        elif input_time >= 160 and input_time < 200:
            output = 4
        elif input_time >= 200 and input_time < 260:
            output =14
        elif input_time >= 260:
            output = 6
        self.appendToSignal(output)