#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   drawio2cbd.py -e Test TestCompute.drawio TestCompute.py

from CBDMultipleOutput.Source.CBD import *
from CBDMultipleOutput.Source.ComputerBlock import ComputerBlock
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Dark2_5 as palette
import itertools

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


class Test(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=[], output_ports=['speed'])
		
		# Create the blocks
		self.addBlock(ComputerBlock(block_name='es2zOFlgJacaEg_o47Cl-33'))
		self.addBlock(Time(block_name='es2zOFlgJacaEg_o47Cl-44'))
		
		# Connect the blocks
		self.addConnection('es2zOFlgJacaEg_o47Cl-33', 'speed')
		self.addConnection('es2zOFlgJacaEg_o47Cl-44', 'es2zOFlgJacaEg_o47Cl-33', output_port_name='time')


class Time(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=[], output_ports=['time', 'deltaT'])
		
		# Create the blocks
		self.addBlock(ConstantBlock(block_name='initTime', value=(0)))
		self.addBlock(DelayBlock(block_name='es2zOFlgJacaEg_o47Cl-9'))
		self.addBlock(AdderBlock(block_name='es2zOFlgJacaEg_o47Cl-16'))
		self.addBlock(ConstantBlock(block_name='h', value=(0.1)))
		
		# Connect the blocks
		self.addConnection('initTime', 'es2zOFlgJacaEg_o47Cl-9', input_port_name='IC')
		self.addConnection('es2zOFlgJacaEg_o47Cl-9', 'time')
		self.addConnection('es2zOFlgJacaEg_o47Cl-9', 'es2zOFlgJacaEg_o47Cl-16')
		self.addConnection('h', 'es2zOFlgJacaEg_o47Cl-16')
		self.addConnection('es2zOFlgJacaEg_o47Cl-16', 'es2zOFlgJacaEg_o47Cl-9')
		self.addConnection('h', 'deltaT')


if __name__ == '__main__':
	cbd = Test("Test")


	# Run the simulation
	cbd.run(3000)

	# process simulation results
	plot_signal(cbd, ['speed'], 'Test computer block')