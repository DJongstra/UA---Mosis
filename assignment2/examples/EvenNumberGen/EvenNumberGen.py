#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   ../../drawio2cbd.py EvenNumberGen.xml EvenNumberGen.py -e EvenNumberGen

from CBDMultipleOutput.Source.CBD import *

from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Dark2_5 as palette
import itertools


def get_block(block, path=""):
	if path == '': return block, block.getBlockName()
	cur = block
	for p in path.split('.'):
		cur = cur.getBlockByName(p)
	return cur, path


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


class Counter(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=[], output_ports=['OutCount'])
		
		# Create the blocks
		self.addBlock(DelayBlock(block_name='delay'))
		self.addBlock(AdderBlock(block_name='sum'))
		self.addBlock(ConstantBlock(block_name='one', value=1.0))
		self.addBlock(ConstantBlock(block_name='zero', value=0.0))
		
		# Connect the blocks
		self.addConnection('zero', 'delay', input_port_name='IC')
		self.addConnection('delay', 'OutCount')
		self.addConnection('delay', 'sum')
		self.addConnection('one', 'sum')
		self.addConnection('sum', 'delay')


class EvenNumberGen(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=[], output_ports=['OutEven'])
		
		# Create the blocks
		self.addBlock(Counter(block_name='counter'))
		self.addBlock(Double(block_name='double'))
		
		# Connect the blocks
		self.addConnection('counter', 'double', input_port_name='InNumber', output_port_name='OutCount')
		self.addConnection('double', 'OutEven', output_port_name='OutDouble')


class Double(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=['InNumber'], output_ports=['OutDouble'])
		
		# Create the blocks
		self.addBlock(ConstantBlock(block_name='two', value=2.0))
		self.addBlock(ProductBlock(block_name='mult'))
		
		# Connect the blocks
		self.addConnection('two', 'mult')
		self.addConnection('InNumber', 'mult')
		self.addConnection('mult', 'OutDouble')


if __name__ == '__main__':
	cbd = EvenNumberGen("EvenNumberGen")


	# Run the simulation
	cbd.run(10)

	# process simulation results
	plot_signal(cbd, ['OutEven'], 'Even Numbers')
