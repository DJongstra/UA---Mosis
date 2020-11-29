#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   drawio2cbd.py -e Random Pseudo-Random.drawio temp.py

from CBDMultipleOutput.Source.CBD import *
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Dark2_5 as palette
import itertools

from ModelsOld.LaTeXGenerator import LaTeXGenerator


def plot_signal(block, signals, title):
    colors = itertools.cycle(palette)
    times = []
    outputs = []

    for signal in signals:
        tvpl = block.getSignal(signal)
        times = [t for t, _ in tvpl]
        outputs.append([v for _, v in tvpl])

    # Plot
    output_file("%s.html" % title.replace(' ', '_').lower(), title=title)
    p = figure(title=title, x_axis_label='time', y_axis_label='N')
    for i in range(len(signals)):
        p.circle(x=times, y=outputs[i], legend_label=signals[i], color=next(colors))
    show(p)


def get_block(block, path=""):
    if path == '': return block, block.getBlockName()
    cur = block
    for p in path.split('.'):
        cur = cur.getBlockByName(p)
    return cur, path


class Random(CBD):
    def __init__(self, block_name, x0=0):
        CBD.__init__(self, block_name, input_ports=[], output_ports=['outRandom'])

        # Create the blocks
        self.addBlock(DelayBlock(block_name='del1'))
        self.addBlock(ProductBlock(block_name='prod1'))
        self.addBlock(ConstantBlock(block_name='a', value=(4)))
        self.addBlock(ConstantBlock(block_name='x0', value=(x0)))
        self.addBlock(AdderBlock(block_name='add1'))
        self.addBlock(ConstantBlock(block_name='c', value=(1)))
        self.addBlock(ModuloBlock(block_name='mod1'))
        self.addBlock(ConstantBlock(block_name='m', value=(9)))

        # Connect the blocks
        self.addConnection('a', 'prod1')
        self.addConnection('del1', 'prod1')
        self.addConnection('x0', 'del1', input_port_name='IC')
        self.addConnection('prod1', 'add1')
        self.addConnection('c', 'add1')
        self.addConnection('add1', 'mod1')
        self.addConnection('mod1', 'del1')
        self.addConnection('m', 'mod1')
        self.addConnection('mod1', 'outRandom')


if __name__ == '__main__':
    for x0 in range(9):
        cbd = Random("Random", x0)

        # Run the simulation
        cbd.run(12)

        tvpl = cbd.getSignal('outRandom')

        output = ([v for _, v in tvpl])
        ind = len(output) - 1 - output[::-1].index(output[0])
        print("period of seed " + str(x0) + " = " + str(ind))

        generator = LaTeXGenerator()
        # generate the LateX
        generator.generateLateX(cbd)


