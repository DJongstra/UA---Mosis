#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   drawio2cbd.py -e IntegratorBlock Integrator2.drawio IntegratorBlock.py

from CBDMultipleOutput.Source.CBD import *


def get_block(block, path=""):
	if path == '': return block, block.getBlockName()
	cur = block
	for p in path.split('.'):
		cur = cur.getBlockByName(p)
	return cur, path


class IntegratedIC(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=['delta_t', 'IC', 'IN1'], output_ports=['OUT1'])
		
		# Create the blocks
		self.addBlock(ProductBlock(block_name='2XOIrNULSFbv1QRsnGYl-43'))
		self.addBlock(NegatorBlock(block_name='2XOIrNULSFbv1QRsnGYl-49'))
		self.addBlock(AdderBlock(block_name='2XOIrNULSFbv1QRsnGYl-53'))
		
		# Connect the blocks
		self.addConnection('delta_t', '2XOIrNULSFbv1QRsnGYl-43')
		self.addConnection('IC', '2XOIrNULSFbv1QRsnGYl-53')
		self.addConnection('IN1', '2XOIrNULSFbv1QRsnGYl-43')
		self.addConnection('2XOIrNULSFbv1QRsnGYl-43', '2XOIrNULSFbv1QRsnGYl-49')
		self.addConnection('2XOIrNULSFbv1QRsnGYl-49', '2XOIrNULSFbv1QRsnGYl-53')
		self.addConnection('2XOIrNULSFbv1QRsnGYl-53', 'OUT1')


class IntegratorBlock(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=['IN1', 'delta_t', 'IC'], output_ports=['OUT1'])
		
		# Create the blocks
		self.addBlock(ProductBlock(block_name='cr9wBLP2Q1uKWm_SEYvH-11'))
		self.addBlock(AdderBlock(block_name='cr9wBLP2Q1uKWm_SEYvH-15'))
		self.addBlock(DelayBlock(block_name='cr9wBLP2Q1uKWm_SEYvH-20'))
		self.addBlock(DelayBlock(block_name='cr9wBLP2Q1uKWm_SEYvH-27'))
		self.addBlock(ConstantBlock(block_name='cr9wBLP2Q1uKWm_SEYvH-32', value=(0)))
		self.addBlock(IntegratedIC(block_name='cr9wBLP2Q1uKWm_SEYvH-35'))
		
		# Connect the blocks
		self.addConnection('IN1', 'cr9wBLP2Q1uKWm_SEYvH-27')
		self.addConnection('delta_t', 'cr9wBLP2Q1uKWm_SEYvH-11')
		self.addConnection('delta_t', 'cr9wBLP2Q1uKWm_SEYvH-35', input_port_name='delta_t')
		self.addConnection('IC', 'cr9wBLP2Q1uKWm_SEYvH-35', input_port_name='IC')
		self.addConnection('cr9wBLP2Q1uKWm_SEYvH-11', 'cr9wBLP2Q1uKWm_SEYvH-15')
		self.addConnection('cr9wBLP2Q1uKWm_SEYvH-15', 'cr9wBLP2Q1uKWm_SEYvH-20')
		self.addConnection('cr9wBLP2Q1uKWm_SEYvH-20', 'cr9wBLP2Q1uKWm_SEYvH-15')
		self.addConnection('cr9wBLP2Q1uKWm_SEYvH-15', 'OUT1')
		self.addConnection('cr9wBLP2Q1uKWm_SEYvH-27', 'cr9wBLP2Q1uKWm_SEYvH-11')
		self.addConnection('cr9wBLP2Q1uKWm_SEYvH-32', 'cr9wBLP2Q1uKWm_SEYvH-27', input_port_name='IC')
		self.addConnection('cr9wBLP2Q1uKWm_SEYvH-27', 'cr9wBLP2Q1uKWm_SEYvH-35')
		self.addConnection('cr9wBLP2Q1uKWm_SEYvH-35', 'cr9wBLP2Q1uKWm_SEYvH-20', input_port_name='IC')


if __name__ == '__main__':
	cbd = IntegratorBlock("IntegratorBlock")


	# Run the simulation
	cbd.run(10)

	# process simulation results
	# TODO: process your results
