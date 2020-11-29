#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   drawio2cbd.py -e Implicit ImplicitEquation.drawio implicit.py

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


class Implicit(CBD):
	def __init__(self, block_name, D=0.1):
		CBD.__init__(self, block_name, input_ports=[], output_ports=['yi', 'xi', 'sinOut'])
		
		# Create the blocks
		self.addBlock(DelayBlock(block_name='x'))
		self.addBlock(ConstantBlock(block_name='x0', value=(0)))
		self.addBlock(DelayBlock(block_name='y'))
		self.addBlock(ConstantBlock(block_name='bknSQExb6rf4TQluvZ8h-15', value=(1)))
		self.addBlock(ConstantBlock(block_name='D', value=(D)))
		self.addBlock(AdderBlock(block_name='addX'))
		self.addBlock(AdderBlock(block_name='addY'))
		self.addBlock(ProductBlock(block_name='bknSQExb6rf4TQluvZ8h-29'))
		self.addBlock(ProductBlock(block_name='bknSQExb6rf4TQluvZ8h-37'))
		self.addBlock(NegatorBlock(block_name='neg'))
		self.addBlock(SinFunc(block_name='bknSQExb6rf4TQluvZ8h-54'))
		
		# Connect the blocks
		self.addConnection('x0', 'x', input_port_name='IC')
		self.addConnection('bknSQExb6rf4TQluvZ8h-15', 'y', input_port_name='IC')
		self.addConnection('addY', 'bknSQExb6rf4TQluvZ8h-29')
		self.addConnection('D', 'bknSQExb6rf4TQluvZ8h-29')
		self.addConnection('bknSQExb6rf4TQluvZ8h-29', 'addX')
		self.addConnection('addY', 'y')
		self.addConnection('addX', 'bknSQExb6rf4TQluvZ8h-37')
		self.addConnection('D', 'bknSQExb6rf4TQluvZ8h-37')
		self.addConnection('bknSQExb6rf4TQluvZ8h-37', 'neg')
		self.addConnection('neg', 'addY')
		self.addConnection('y', 'addY')
		self.addConnection('x', 'addX')
		self.addConnection('addX', 'x')
		self.addConnection('addY', 'yi')
		self.addConnection('addX', 'xi')
		self.addConnection('D', 'bknSQExb6rf4TQluvZ8h-54', input_port_name='Din')
		self.addConnection('bknSQExb6rf4TQluvZ8h-54', 'sinOut', output_port_name='sinOut')


if __name__ == '__main__':
	D = 0.001
	cbd = Implicit("Implicit", D)

	steps = int((2 * math.pi) / D)

	# Run the simulation
	cbd.run(steps)
	plot_signal(cbd, ['xi', 'yi', 'sinOut'], 'Implicit')

	generator = LaTeXGenerator()
	# generate the LateX
	generator.generateLateX(cbd)

