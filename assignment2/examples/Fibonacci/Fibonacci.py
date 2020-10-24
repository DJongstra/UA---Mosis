#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   ../../drawio2cbd.py Fibonacci.xml Fibonacci.py -e FibonacciGen

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


class InitialConditions(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=[], output_ports=['OUT1', 'OUT2', 'OUT3'])
		
		# Create the blocks
		self.addBlock(ConstantBlock(block_name='one', value=1.0))
		self.addBlock(ConstantBlock(block_name='two', value=2.0))
		self.addBlock(AdderBlock(block_name='sum1'))
		self.addBlock(AdderBlock(block_name='sum2'))
		self.addBlock(NegatorBlock(block_name='neg1'))
		self.addBlock(NegatorBlock(block_name='neg2'))
		self.addBlock(RootBlock(block_name='root'))
		
		# Connect the blocks
		self.addConnection('one', 'neg2')
		self.addConnection('one', 'root')
		self.addConnection('two', 'sum1')
		self.addConnection('two', 'root')
		self.addConnection('sum1', 'sum2')
		self.addConnection('sum1', 'neg1')
		self.addConnection('neg1', 'sum1')
		self.addConnection('neg2', 'sum2')
		self.addConnection('sum1', 'OUT1')
		self.addConnection('sum2', 'OUT2')
		self.addConnection('root', 'OUT3')


class FibonacciGen(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=[], output_ports=['OutFib'])
		
		# Create the blocks
		self.addBlock(InitialConditions(block_name='conditions'))
		self.addBlock(DelayBlock(block_name='D1'))
		self.addBlock(DelayBlock(block_name='D2'))
		self.addBlock(DelayBlock(block_name='D3'))
		self.addBlock(AdderBlock(block_name='sum'))
		
		# Connect the blocks
		self.addConnection('conditions', 'D1', input_port_name='IC')
		self.addConnection('conditions', 'D2', input_port_name='IC', output_port_name='OUT2')
		self.addConnection('conditions', 'D3', input_port_name='IC', output_port_name='OUT3')
		self.addConnection('D1', 'D2')
		self.addConnection('D1', 'sum')
		self.addConnection('D2', 'sum')
		self.addConnection('D3', 'OutFib')
		self.addConnection('sum', 'D1')
		self.addConnection('sum', 'D3')


if __name__ == '__main__':
	cbd = FibonacciGen("fibonacci_gen")


	# Run the simulation
	cbd.run(10)

	# process simulation results
	plot_signal(cbd, ['OutFib'], 'Fibonacci Numbers')
