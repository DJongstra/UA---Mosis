#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   drawio2cbd.py -e Explicit ExplicitEquation.drawio temp.py

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


class Explicit(CBD):
	def __init__(self, block_name, D=0.1):
		CBD.__init__(self, block_name, input_ports=[], output_ports=['xi', 'yi', 'sinOut'])
		
		# Create the blocks
		self.addBlock(DelayBlock(block_name='x'))
		self.addBlock(ConstantBlock(block_name='x0', value=(0)))
		self.addBlock(DelayBlock(block_name='y'))
		self.addBlock(ConstantBlock(block_name='y0', value=(1)))
		self.addBlock(ConstantBlock(block_name='D', value=(D)))
		self.addBlock(ProductBlock(block_name='mulX'))
		self.addBlock(AdderBlock(block_name='sumX'))
		self.addBlock(ProductBlock(block_name='mulY'))
		self.addBlock(NegatorBlock(block_name='negDX'))
		self.addBlock(AdderBlock(block_name='sumY'))
		self.addBlock(SinFunc(block_name='sin'))
		
		# Connect the blocks
		self.addConnection('x0', 'x', input_port_name='IC')
		self.addConnection('y0', 'y', input_port_name='IC')
		self.addConnection('y', 'mulX')
		self.addConnection('D', 'mulX')
		self.addConnection('x', 'sumX')
		self.addConnection('mulX', 'sumX')
		self.addConnection('sumX', 'x')
		self.addConnection('sumX', 'xi')
		self.addConnection('x', 'mulY')
		self.addConnection('D', 'mulY')
		self.addConnection('mulY', 'negDX')
		self.addConnection('y', 'sumY')
		self.addConnection('negDX', 'sumY')
		self.addConnection('sumY', 'y')
		self.addConnection('sumY', 'yi')
		self.addConnection('D', 'sin', input_port_name='Din')
		self.addConnection('sin', 'sinOut', output_port_name='sinOut')


class SinFunc(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=['Din'], output_ports=['sinOut'])
		
		# Create the blocks
		self.addBlock(TimeBlock(block_name='time'))
		self.addBlock(ProductBlock(block_name='prodSin'))
		self.addBlock(GenericBlock(block_name='sin', block_operator=("sin")))
		
		# Connect the blocks
		self.addConnection('time', 'prodSin')
		self.addConnection('Din', 'prodSin')
		self.addConnection('prodSin', 'sin')
		self.addConnection('sin', 'sinOut')


if __name__ == '__main__':
	D = 0.001
	cbd = Explicit("Explicit", D)

	steps = int((2 * math.pi) / D)


	# Run the simulation
	cbd.run(steps)
	plot_signal(cbd, ['xi', 'yi', 'sinOut'], 'Explicit')

	generator = LaTeXGenerator()
	# generate the LateX
	generator.generateLateX(cbd)