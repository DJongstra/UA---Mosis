#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   ../../drawio2cbd.py SinGen.xml SinGen.py -e SinGen

from CBDMultipleOutput.Source.CBD import *


import matplotlib.pyplot as plt


def plot_signals(block, signals, title):
	times = []
	outputs = []

	for signal in signals:
		tvpl = block.getSignal(signal)
		times = [t for t, _ in tvpl]
		outputs.append([v for _, v in tvpl])

	# Plot
	plt.figure()
	plt.title(title)
	plt.xlabel('time')
	plt.ylabel('N')
	for i in range(len(signals)):
		plt.scatter(times, outputs[i], label=signals[i])
	plt.legend()
	plt.show()



def get_block(block, path=""):
	if path == '': return block, block.getBlockName()
	cur = block
	for p in path.split('.'):
		cur = cur.getBlockByName(p)
	return cur, path


class SinGen(CBD):
	def __init__(self, block_name, test=("Bla bla \n test")):
		CBD.__init__(self, block_name, input_ports=[], output_ports=['OUT1'])
		
		# Create the blocks
		self.addBlock(TimeBlock(block_name='time'))
		self.addBlock(GenericBlock(block_name='sin', block_operator=("sin")))
		
		# Connect the blocks
		self.addConnection('time', 'sin')
		self.addConnection('sin', 'OUT1')


if __name__ == '__main__':
	cbd = SinGen("SinGen")
	print(cbd.latex())


	# Run the simulation
	cbd.run(10)

	# process simulation results
	plot_signals(cbd, ['OUT1'], 'Sine Function')
