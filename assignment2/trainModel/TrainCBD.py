#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   drawio2cbd.py -e TrainCBD TrainCBD.drawio TrainCBD.py

from CBDMultipleOutput.Source.CBD import *
from trainModel.ComputerBlock import ComputerBlock
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Dark2_5 as palette
import itertools

from trainModel.TrainCostModelBlock import CostFunctionBlock


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


class PIDControllerBlock(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=['delta_v', 'delta_t', 'Kd', 'Ki', 'Kp'], output_ports=['OUT_TRACTION'])
		
		# Create the blocks
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
		self.addConnection('Kp', 'prodKpDv')
		self.addConnection('delta_t', 'integral', input_port_name='delta_t')
		self.addConnection('delta_t', 'derivative', input_port_name='delta_t')
		self.addConnection('integral', 'prodKiIntDvDt')
		self.addConnection('Ki', 'prodKiIntDvDt')
		self.addConnection('Kd', 'prodKdDvdt')
		self.addConnection('derivative', 'prodKdDvdt')
		self.addConnection('prodKpDv', 'sum1')
		self.addConnection('prodKiIntDvDt', 'sum1')
		self.addConnection('sum1', 'sum2')
		self.addConnection('prodKdDvdt', 'sum2')
		self.addConnection('sum2', 'OUT_TRACTION')


class TrainCBD(CBD):
	def __init__(self, block_name, Kd=(0), Ki=(0), Kp=(200)):
		CBD.__init__(self, block_name, input_ports=[], output_ports=['V_TRAIN', 'IDEAL_VTRAIN', 'X_PASSENGER', 'OUT_DELTA', 'A_TRAIN', 'A_PASSENGER'])

		print("TrainCBD >> [ Kd = {}, Ki = {}, Kp = {} ]".format(Kd, Ki, Kp))
		# Create the blocks
		self.addBlock(TrainTimeBlock(block_name='ttb1'))
		self.addBlock(ComputerBlock(block_name='cb1'))
		self.addBlock(AdderBlock(block_name='sum1'))
		self.addBlock(NegatorBlock(block_name='negator1'))
		self.addBlock(PlantBlock(block_name='pl1'))
		self.addBlock(PIDControllerBlock(block_name='pid1'))
		self.addBlock(ConstantBlock(block_name='KI', value=(Ki)))
		self.addBlock(ConstantBlock(block_name='KD', value=(Kd)))
		self.addBlock(ConstantBlock(block_name='KP', value=(Kp)))
		
		# Connect the blocks
		self.addConnection('cb1', 'sum1')
		self.addConnection('sum1', 'pid1', input_port_name='delta_v')
		self.addConnection('ttb1', 'pid1', input_port_name='delta_t', output_port_name='OUT_DELTA')
		self.addConnection('ttb1', 'pl1', input_port_name='delta_t', output_port_name='OUT_DELTA')
		self.addConnection('negator1', 'sum1')
		self.addConnection('pid1', 'pl1', input_port_name='F_Traction', output_port_name='OUT_TRACTION')
		self.addConnection('ttb1', 'cb1')
		self.addConnection('cb1', 'IDEAL_VTRAIN')
		self.addConnection('pl1', 'negator1', output_port_name='vTrain')
		self.addConnection('pl1', 'V_TRAIN', output_port_name='vTrain')
		self.addConnection('pl1', 'X_PASSENGER', output_port_name='xPassenger')
		self.addConnection('ttb1', 'OUT_DELTA', output_port_name='OUT_DELTA')
		self.addConnection('KD', 'pid1', input_port_name='Kd')
		self.addConnection('KP', 'pid1', input_port_name='Kp')
		self.addConnection('KI', 'pid1', input_port_name='Ki')
		self.addConnection('pl1', 'A_TRAIN', output_port_name='aTrain')
		self.addConnection('pl1', 'A_PASSENGER', output_port_name='aPassenger')


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


class TrainBlock(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=['F_Traction', 'delta_t'], output_ports=['OUT_vtrain', 'OUT_atrain'])
		
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
		self.addConnection('product6', 'OUT_atrain')


class PassengerBlock(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=['F_Traction', 'delta_t'], output_ports=['OUT_xPassenger', 'OUT_aPassenger'])
		
		# Create the blocks
		self.addBlock(ConstantBlock(block_name='mTrain', value=(5555)))
		self.addBlock(ConstantBlock(block_name='mPassenger', value=(73)))
		self.addBlock(AdderBlock(block_name='sum1'))
		self.addBlock(InverterBlock(block_name='inverter1'))
		self.addBlock(ProductBlock(block_name='product1'))
		self.addBlock(ProductBlock(block_name='product4'))
		self.addBlock(NegatorBlock(block_name='negator1'))
		self.addBlock(NegatorBlock(block_name='negator2'))
		self.addBlock(ConstantBlock(block_name='k', value=(300)))
		self.addBlock(ConstantBlock(block_name='c', value=(150)))
		self.addBlock(ProductBlock(block_name='product2'))
		self.addBlock(ProductBlock(block_name='product3'))
		self.addBlock(AdderBlock(block_name='sum2'))
		self.addBlock(AdderBlock(block_name='sum3'))
		self.addBlock(IntegratorBlock(block_name='integral1'))
		self.addBlock(ConstantBlock(block_name='IC', value=(0)))
		self.addBlock(IntegratorBlock(block_name='integral2'))
		self.addBlock(NegatorBlock(block_name='negator3'))
		self.addBlock(InverterBlock(block_name='inverter2'))
		self.addBlock(ProductBlock(block_name='product5'))
		
		# Connect the blocks
		self.addConnection('mTrain', 'sum1')
		self.addConnection('mPassenger', 'sum1')
		self.addConnection('sum1', 'inverter1')
		self.addConnection('F_Traction', 'product1')
		self.addConnection('inverter1', 'product1')
		self.addConnection('product1', 'product4')
		self.addConnection('mPassenger', 'product4')
		self.addConnection('product4', 'negator1')
		self.addConnection('negator2', 'product2')
		self.addConnection('k', 'product2')
		self.addConnection('c', 'product3')
		self.addConnection('product2', 'sum2')
		self.addConnection('product3', 'sum2')
		self.addConnection('negator1', 'sum3')
		self.addConnection('sum2', 'sum3')
		self.addConnection('IC', 'integral1', input_port_name='IC')
		self.addConnection('integral1', 'negator3')
		self.addConnection('IC', 'integral2', input_port_name='IC')
		self.addConnection('integral2', 'negator2')
		self.addConnection('integral1', 'integral2')
		self.addConnection('integral2', 'OUT_xPassenger')
		self.addConnection('delta_t', 'integral1', input_port_name='delta_t')
		self.addConnection('delta_t', 'integral2', input_port_name='delta_t')
		self.addConnection('negator3', 'product3')
		self.addConnection('mPassenger', 'inverter2')
		self.addConnection('inverter2', 'product5')
		self.addConnection('sum3', 'product5')
		self.addConnection('product5', 'integral1')
		self.addConnection('integral1', 'OUT_aPassenger')


class PlantBlock(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=['F_Traction', 'delta_t'], output_ports=['xPassenger', 'vTrain', 'aTrain', 'aPassenger'])
		
		# Create the blocks
		self.addBlock(PassengerBlock(block_name='pa'))
		self.addBlock(TrainBlock(block_name='tr'))
		
		# Connect the blocks
		self.addConnection('F_Traction', 'tr', input_port_name='F_Traction')
		self.addConnection('F_Traction', 'pa', input_port_name='F_Traction')
		self.addConnection('delta_t', 'tr', input_port_name='delta_t')
		self.addConnection('delta_t', 'pa', input_port_name='delta_t')
		self.addConnection('tr', 'vTrain', output_port_name='OUT_vtrain')
		self.addConnection('pa', 'xPassenger', output_port_name='OUT_xPassenger')
		self.addConnection('tr', 'aTrain', output_port_name='OUT_atrain')
		self.addConnection('pa', 'aPassenger', output_port_name='OUT_aPassenger')


class TrainTuningBlock(CBD):
	def __init__(self, block_name, Kd=(0), Ki=(0), Kp=(200)):
		CBD.__init__(self, block_name, input_ports=[], output_ports=['OUT_COST'])
		
		# Create the blocks
		self.addBlock(CostFunctionBlock(block_name='cfb1'))
		print("TrainTuningBlock >> [ Kd = {}, Ki = {}, Kp = {} ]".format(Kd, Ki, Kp))
		self.addBlock(TrainCBD(block_name='trc1',Kd =Kd, Ki=Ki, Kp=Kp))
		
		# Connect the blocks
		self.addConnection('trc1', 'cfb1', input_port_name='InVTrain', output_port_name='V_TRAIN')
		self.addConnection('trc1', 'cfb1', input_port_name='InXPerson', output_port_name='X_PASSENGER')
		self.addConnection('trc1', 'cfb1', input_port_name='InDelta', output_port_name='OUT_DELTA')
		self.addConnection('trc1', 'cfb1', input_port_name='InVi', output_port_name='IDEAL_VTRAIN')
		self.addConnection('cfb1', 'OUT_COST', output_port_name='OutCost')


if __name__ == '__main__':
	cbd = TrainCBD("TrainCBD")

	# Run the simulation
	cbd.run(3500)

	# process simulation results
	plot_signal(cbd, ['IDEAL_VTRAIN', 'V_TRAIN' ], 'Ideal and Actual velocityof train (200,0,0)')
	plot_signal(cbd, ['X_PASSENGER','A_TRAIN'], 'Person Displacement and Train acceleration (200,0,0)')
