#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   drawio2cbd.py -e TrainCBD TrainCBD.drawio TrainCBD.py

from CBDMultipleOutput.Source.CBD import *
from ComputerBlock import ComputerBlock


def get_block(block, path=""):
	if path == '': return block, block.getBlockName()
	cur = block
	for p in path.split('.'):
		cur = cur.getBlockByName(p)
	return cur, path


class PIDControllerBlock(CBD):
	def __init__(self, block_name, Kp=(200), Ki=(0), Kd=(0)):
		CBD.__init__(self, block_name, input_ports=['delta_v', 'delta_t'], output_ports=['OUT_TRACTION'])
		
		# Create the blocks
		self.addBlock(ConstantBlock(block_name='KI', value=(Ki)))
		self.addBlock(ConstantBlock(block_name='KP', value=(Kp)))
		self.addBlock(ConstantBlock(block_name='KD', value=(Kd)))
		self.addBlock(ProductBlock(block_name='prodKpDv'))
		self.addBlock(IntegratorBlock(block_name='integral'))
		self.addBlock(ProductBlock(block_name='prodKiIntDvDt'))
		self.addBlock(DerivatorBlock(block_name='derivative'))
		self.addBlock(ProductBlock(block_name='prodKdDvdt'))
		self.addBlock(AdderBlock(block_name='sum1'))
		self.addBlock(AdderBlock(block_name='sum2'))
		
		# Connect the blocks
		self.addConnection('delta_v', 'derivative')
		self.addConnection('delta_v', 'prodKpDv')
		self.addConnection('delta_v', 'integral')
		self.addConnection('delta_v', 'derivative', input_port_name='IC')
		self.addConnection('delta_v', 'integral', input_port_name='IC')
		self.addConnection('KP', 'prodKpDv')
		self.addConnection('delta_t', 'integral', input_port_name='delta_t')
		self.addConnection('delta_t', 'derivative', input_port_name='delta_t')
		self.addConnection('integral', 'prodKiIntDvDt')
		self.addConnection('KI', 'prodKiIntDvDt')
		self.addConnection('KD', 'prodKdDvdt')
		self.addConnection('derivative', 'prodKdDvdt')
		self.addConnection('prodKpDv', 'sum1')
		self.addConnection('prodKiIntDvDt', 'sum1')
		self.addConnection('sum1', 'sum2')
		self.addConnection('prodKdDvdt', 'sum2')
		self.addConnection('sum2', 'OUT_TRACTION')


class TrainCBD(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=[], output_ports=['V_TRAIN', 'OUT_CB'])
		
		# Create the blocks
		self.addBlock(TrainTimeBlock(block_name='ttb1'))
		self.addBlock(PlantBlock(block_name='pl1'))
		self.addBlock(PIDControllerBlock(block_name='pid1'))
		self.addBlock(ComputerBlock(block_name='cb1'))
		self.addBlock(AdderBlock(block_name='sum1'))
		self.addBlock(NegatorBlock(block_name='negator1'))
		
		# Connect the blocks
		self.addConnection('cb1', 'sum1')
		self.addConnection('pl1', 'negator1', output_port_name='OUT_vtrain')
		self.addConnection('sum1', 'pid1', input_port_name='delta_v')
		self.addConnection('ttb1', 'pid1', input_port_name='delta_t', output_port_name='OUT_DELTA')
		self.addConnection('ttb1', 'pl1', input_port_name='delta_t', output_port_name='OUT_DELTA')
		self.addConnection('negator1', 'sum1')
		self.addConnection('pid1', 'pl1', input_port_name='F_Traction', output_port_name='OUT_TRACTION')
		self.addConnection('pl1', 'V_TRAIN', output_port_name='OUT_vtrain')
		self.addConnection('ttb1', 'cb1')


class TrainTimeBlock(CBD):
	def __init__(self, block_name, h=(0.1)):
		CBD.__init__(self, block_name, input_ports=[], output_ports=['OUT_DELTA', 'OUT1'])
		
		# Create the blocks
		self.addBlock(ConstantBlock(block_name='zero', value=(0)))
		self.addBlock(DelayBlock(block_name='delay1'))
		self.addBlock(AdderBlock(block_name='sum1'))
		self.addBlock(ConstantBlock(block_name='h', value=(h)))
		
		# Connect the blocks
		self.addConnection('zero', 'delay1', input_port_name='IC')
		self.addConnection('delay1', 'sum1')
		self.addConnection('sum1', 'delay1')
		self.addConnection('h', 'sum1')
		self.addConnection('h', 'OUT_DELTA')
		self.addConnection('delay1', 'OUT1')


class PlantBlock(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=['F_Traction', 'delta_t'], output_ports=['OUT_vtrain'])
		
		# Create the blocks
		self.addBlock(ConstantBlock(block_name='IC', value=(0)))
		self.addBlock(IntegratorBlock(block_name='integral1'))
		self.addBlock(ProductBlock(block_name='product1'))
		self.addBlock(ConstantBlock(block_name='p', value=(1.2)))
		self.addBlock(ProductBlock(block_name='product2'))
		self.addBlock(ConstantBlock(block_name='Cd', value=(0.6)))
		self.addBlock(ProductBlock(block_name='product3'))
		self.addBlock(ConstantBlock(block_name='A', value=(9.12)))
		self.addBlock(ProductBlock(block_name='product4'))
		self.addBlock(ConstantBlock(block_name='Two', value=(2)))
		self.addBlock(InverterBlock(block_name='inverter1'))
		self.addBlock(ProductBlock(block_name='product5'))
		self.addBlock(NegatorBlock(block_name='negator1'))
		self.addBlock(AdderBlock(block_name='sum1'))
		self.addBlock(ConstantBlock(block_name='mTrain', value=(5555)))
		self.addBlock(ConstantBlock(block_name='mPassenger', value=(73)))
		self.addBlock(AdderBlock(block_name='sum2'))
		self.addBlock(InverterBlock(block_name='inverter2'))
		self.addBlock(ProductBlock(block_name='product6'))
		
		# Connect the blocks
		self.addConnection('F_Traction', 'sum1')
		self.addConnection('delta_t', 'integral1', input_port_name='delta_t')
		self.addConnection('IC', 'integral1', input_port_name='IC')
		self.addConnection('integral1', 'product1')
		self.addConnection('integral1', 'product1')
		self.addConnection('p', 'product2')
		self.addConnection('product1', 'product2')
		self.addConnection('Cd', 'product3')
		self.addConnection('product2', 'product3')
		self.addConnection('A', 'product4')
		self.addConnection('product3', 'product4')
		self.addConnection('Two', 'inverter1')
		self.addConnection('inverter1', 'product5')
		self.addConnection('product4', 'product5')
		self.addConnection('product5', 'negator1')
		self.addConnection('negator1', 'sum1')
		self.addConnection('mTrain', 'sum2')
		self.addConnection('mPassenger', 'sum2')
		self.addConnection('sum2', 'inverter2')
		self.addConnection('inverter2', 'product6')
		self.addConnection('sum1', 'product6')
		self.addConnection('product6', 'integral1')
		self.addConnection('integral1', 'OUT_vtrain')


if __name__ == '__main__':
	cbd = TrainCBD("TrainCBD")


	# Run the simulation
	cbd.run(10)

	# process simulation results
	# TODO: process your results
