#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   drawio2cbd.py -e CBDB CBDB CBDB.py

from CBDMultipleOutput.Source.CBD import *
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


class CBDB(CBD):
	def __init__(self, block_name, deltaT=0.1):
		CBD.__init__(self, block_name, input_ports=[], output_ports=['OUT1'])
		
		# Create the blocks
		self.addBlock(DelayBlock(block_name='x'))
		self.addBlock(ConstantBlock(block_name='x0', value=(0)))
		self.addBlock(DerivatorBlock(block_name='WgBMcyxID5A1E6gqlP3p-11'))
		self.addBlock(DerivatorBlock(block_name='WgBMcyxID5A1E6gqlP3p-17'))
		self.addBlock(ConstantBlock(block_name='initdxdt', value=(1)))
		self.addBlock(NegatorBlock(block_name='WgBMcyxID5A1E6gqlP3p-31'))
		self.addBlock(ConstantBlock(block_name='deltaT', value=(deltaT)))
		
		# Connect the blocks
		self.addConnection('x0', 'x', input_port_name='IC')
		self.addConnection('x', 'WgBMcyxID5A1E6gqlP3p-11')
		self.addConnection('WgBMcyxID5A1E6gqlP3p-11', 'WgBMcyxID5A1E6gqlP3p-17')
		self.addConnection('initdxdt', 'WgBMcyxID5A1E6gqlP3p-11', input_port_name='IC')
		self.addConnection('WgBMcyxID5A1E6gqlP3p-17', 'WgBMcyxID5A1E6gqlP3p-31')
		self.addConnection('WgBMcyxID5A1E6gqlP3p-31', 'x')
		self.addConnection('WgBMcyxID5A1E6gqlP3p-31', 'OUT1')
		self.addConnection('deltaT', 'WgBMcyxID5A1E6gqlP3p-11', input_port_name='delta_t')
		self.addConnection('deltaT', 'WgBMcyxID5A1E6gqlP3p-17', input_port_name='delta_t')
		self.addConnection('WgBMcyxID5A1E6gqlP3p-11', 'WgBMcyxID5A1E6gqlP3p-17', input_port_name='IC')


if __name__ == '__main__':
	cbd = CBDB("CBDB")


	# Run the simulation
	cbd.run(100)

	# process simulation results
	plot_signal(cbd, ['OUT1'], 'Harmonic B')
