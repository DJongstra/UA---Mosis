#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   drawio2cbd.py -e DerivatorBlock Derivator.drawio DerivatorBlock.py

from CBDMultipleOutput.Source.CBD import *


def get_block(block, path=""):
	if path == '': return block, block.getBlockName()
	cur = block
	for p in path.split('.'):
		cur = cur.getBlockByName(p)
	return cur, path


class DerivedIC(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=['IC', 'IN1', 'delta_t'], output_ports=['dIC'])
		
		# Create the blocks
		self.addBlock(ProductBlock(block_name='product'))
		self.addBlock(NegatorBlock(block_name='negative'))
		self.addBlock(AdderBlock(block_name='sum'))
		
		# Connect the blocks
		self.addConnection('IC', 'product')
		self.addConnection('IN1', 'sum')
		self.addConnection('delta_t', 'product')
		self.addConnection('product', 'negative')
		self.addConnection('negative', 'sum')
		self.addConnection('sum', 'dIC')


class DerivatorBlock(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=['IN1', 'IC', 'delta_t'], output_ports=['OUT1'])
		
		# Create the blocks
		self.addBlock(DelayBlock(block_name='delay'))
		self.addBlock(DerivedIC(block_name='derivedIC'))
		self.addBlock(NegatorBlock(block_name='negator'))
		self.addBlock(AdderBlock(block_name='xRnvEjVIsQNWptp_Bo56-33'))
		self.addBlock(ProductBlock(block_name='product'))
		self.addBlock(InverterBlock(block_name='inverter'))
		
		# Connect the blocks
		self.addConnection('IN1', 'derivedIC')
		self.addConnection('IN1', 'delay')
		self.addConnection('IN1', 'xRnvEjVIsQNWptp_Bo56-33')
		self.addConnection('IC', 'derivedIC', input_port_name='IC')
		self.addConnection('delta_t', 'derivedIC', input_port_name='delta_t')
		self.addConnection('delta_t', 'inverter')
		self.addConnection('derivedIC', 'delay', input_port_name='IC', output_port_name='dIC')
		self.addConnection('delay', 'negator')
		self.addConnection('negator', 'xRnvEjVIsQNWptp_Bo56-33')
		self.addConnection('xRnvEjVIsQNWptp_Bo56-33', 'product')
		self.addConnection('inverter', 'product')
		self.addConnection('product', 'OUT1')


if __name__ == '__main__':
	cbd = DerivatorBlock("DerivatorBlock")


	# Run the simulation
	cbd.run(10)

	# process simulation results
	# TODO: process your results
