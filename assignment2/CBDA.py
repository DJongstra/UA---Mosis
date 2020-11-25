#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   drawio2cbd.py -e CBDA CBDA.drawio CBDA.py

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


class CBDA(CBD):
	def __init__(self, block_name, deltaT=0.1):
		CBD.__init__(self, block_name, input_ports=[], output_ports=['OUT1', 'error'])
		
		# Create the blocks
		self.addBlock(ConstantBlock(block_name='x0', value=(0)))
		self.addBlock(ConstantBlock(block_name='initdxdt', value=(-1)))
		self.addBlock(NegatorBlock(block_name='WgBMcyxID5A1E6gqlP3p-31'))
		self.addBlock(ConstantBlock(block_name='deltaT', value=(deltaT)))
		self.addBlock(IntegratorBlock(block_name='7IsC0muY9sn0-m5gdAO--8'))
		self.addBlock(IntegratorBlock(block_name='7IsC0muY9sn0-m5gdAO--14'))
		self.addBlock(SinFunc(block_name='qr4DKPYwkg5aO8gcdtgf-35'))
		self.addBlock(AdderBlock(block_name='qr4DKPYwkg5aO8gcdtgf-39'))
		self.addBlock(ABSBlock(block_name='qr4DKPYwkg5aO8gcdtgf-45'))
		self.addBlock(IntegratorBlock(block_name='qr4DKPYwkg5aO8gcdtgf-49'))
		self.addBlock(ConstantBlock(block_name='qr4DKPYwkg5aO8gcdtgf-60', value=(0)))
		
		# Connect the blocks
		self.addConnection('deltaT', '7IsC0muY9sn0-m5gdAO--8', input_port_name='delta_t')
		self.addConnection('deltaT', '7IsC0muY9sn0-m5gdAO--14', input_port_name='delta_t')
		self.addConnection('7IsC0muY9sn0-m5gdAO--14', 'WgBMcyxID5A1E6gqlP3p-31')
		self.addConnection('WgBMcyxID5A1E6gqlP3p-31', 'OUT1')
		self.addConnection('7IsC0muY9sn0-m5gdAO--8', '7IsC0muY9sn0-m5gdAO--14')
		self.addConnection('initdxdt', '7IsC0muY9sn0-m5gdAO--8', input_port_name='IC')
		self.addConnection('x0', '7IsC0muY9sn0-m5gdAO--14', input_port_name='IC')
		self.addConnection('WgBMcyxID5A1E6gqlP3p-31', '7IsC0muY9sn0-m5gdAO--8')
		self.addConnection('deltaT', 'qr4DKPYwkg5aO8gcdtgf-35', input_port_name='Din')
		self.addConnection('qr4DKPYwkg5aO8gcdtgf-35', 'qr4DKPYwkg5aO8gcdtgf-39', output_port_name='sinOut')
		self.addConnection('7IsC0muY9sn0-m5gdAO--14', 'qr4DKPYwkg5aO8gcdtgf-39')
		self.addConnection('qr4DKPYwkg5aO8gcdtgf-39', 'qr4DKPYwkg5aO8gcdtgf-45')
		self.addConnection('qr4DKPYwkg5aO8gcdtgf-45', 'qr4DKPYwkg5aO8gcdtgf-49')
		self.addConnection('deltaT', 'qr4DKPYwkg5aO8gcdtgf-49', input_port_name='delta_t')
		self.addConnection('qr4DKPYwkg5aO8gcdtgf-49', 'error')
		self.addConnection('qr4DKPYwkg5aO8gcdtgf-60', 'qr4DKPYwkg5aO8gcdtgf-49', input_port_name='IC')


class SinFunc(CBD):
	def __init__(self, block_name):
		CBD.__init__(self, block_name, input_ports=['Din'], output_ports=['sinOut'])
		
		# Create the blocks
		self.addBlock(TimeBlock(block_name='time'))
		self.addBlock(ProductBlock(block_name='prodSin'))
		self.addBlock(GenericBlock(block_name='sin', block_operator=("sin")))
		
		# Connect the blocks
		self.addConnection('time', 'prodSin')
		self.addConnection('Din', 'prodSin')
		self.addConnection('prodSin', 'sin')
		self.addConnection('sin', 'sinOut')


if __name__ == '__main__':
	cbd = CBDA("CBDA")


	# Run the simulation
	cbd.run(200)

	# process simulation results
	plot_signal(cbd, ['OUT1'], 'Harmonic A')
	plot_signal(cbd, ['error'], 'Error Harmonic A')
