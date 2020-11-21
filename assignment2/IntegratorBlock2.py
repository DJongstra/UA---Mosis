#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   drawio2cbd.py -e IntegratorBlock Integrator2.drawio IntegratorBlock2.py

from CBDMultipleOutput.Source.CBD import *


def get_block(block, path=""):
	if path == '': return block, block.getBlockName()
	cur = block
	for p in path.split('.'):
		cur = cur.getBlockByName(p)
	return cur, path


class IntegratorBlock(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=['IN1', 'delta_t', 'IC'], output_ports=['OUT1'])
		
		# Create the blocks
		self.addBlock(ProductBlock(block_name='2XOIrNULSFbv1QRsnGYl-13'))
		self.addBlock(AdderBlock(block_name='2XOIrNULSFbv1QRsnGYl-20'))
		self.addBlock(DelayBlock(block_name='2XOIrNULSFbv1QRsnGYl-26'))
		self.addBlock(IntegratedIC(block_name='2XOIrNULSFbv1QRsnGYl-70'))
		self.addBlock(DelayBlock(block_name='m2JUptWFHnOxhU3OeOcB-1'))
		
		# Connect the blocks
		self.addConnection('IN1', '2XOIrNULSFbv1QRsnGYl-70')
		self.addConnection('IN1', 'm2JUptWFHnOxhU3OeOcB-1')
		self.addConnection('IN1', 'm2JUptWFHnOxhU3OeOcB-1', input_port_name='IC')
		self.addConnection('delta_t', '2XOIrNULSFbv1QRsnGYl-13')
		self.addConnection('delta_t', '2XOIrNULSFbv1QRsnGYl-70', input_port_name='delta_t')
		self.addConnection('IC', '2XOIrNULSFbv1QRsnGYl-70', input_port_name='IC')
		self.addConnection('2XOIrNULSFbv1QRsnGYl-13', '2XOIrNULSFbv1QRsnGYl-20')
		self.addConnection('2XOIrNULSFbv1QRsnGYl-20', '2XOIrNULSFbv1QRsnGYl-26')
		self.addConnection('2XOIrNULSFbv1QRsnGYl-26', '2XOIrNULSFbv1QRsnGYl-20')
		self.addConnection('2XOIrNULSFbv1QRsnGYl-20', 'OUT1')
		self.addConnection('2XOIrNULSFbv1QRsnGYl-70', '2XOIrNULSFbv1QRsnGYl-26', input_port_name='IC')
		self.addConnection('m2JUptWFHnOxhU3OeOcB-1', '2XOIrNULSFbv1QRsnGYl-13')


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


if __name__ == '__main__':
	cbd = IntegratorBlock("IntegratorBlock")


	# Run the simulation
	cbd.run(10)

	# process simulation results
	# TODO: process your results
