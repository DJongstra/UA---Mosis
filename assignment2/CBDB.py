#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   drawio2cbd.py -e CBDB CBDB.drawio CBDB.py

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
		CBD.__init__(self, block_name, input_ports=[], output_ports=['OUT1', 'error'])
		
		# Create the blocks
		self.addBlock(ConstantBlock(block_name='x0', value=(0)))
		self.addBlock(ConstantBlock(block_name='initdxdt', value=(1)))
		self.addBlock(NegatorBlock(block_name='WgBMcyxID5A1E6gqlP3p-31'))
		self.addBlock(ConstantBlock(block_name='deltaT', value=(deltaT)))
		self.addBlock(DerivatorBlock(block_name='CZ0sbhZwY290FykPwCE_-1'))
		self.addBlock(DerivatorBlock(block_name='CZ0sbhZwY290FykPwCE_-6'))
		self.addBlock(SinFunc(block_name='kQCSEosvlVg2ZfA-_8SE-22'))
		self.addBlock(AdderBlock(block_name='kQCSEosvlVg2ZfA-_8SE-26'))
		self.addBlock(ABSBlock(block_name='kQCSEosvlVg2ZfA-_8SE-32'))
		self.addBlock(ConstantBlock(block_name='kQCSEosvlVg2ZfA-_8SE-43', value=(0)))
		self.addBlock(IntegratorBlock(block_name='kQCSEosvlVg2ZfA-_8SE-36'))
		
		# Connect the blocks
		self.addConnection('WgBMcyxID5A1E6gqlP3p-31', 'OUT1')
		self.addConnection('CZ0sbhZwY290FykPwCE_-6', 'WgBMcyxID5A1E6gqlP3p-31')
		self.addConnection('CZ0sbhZwY290FykPwCE_-1', 'CZ0sbhZwY290FykPwCE_-6')
		self.addConnection('deltaT', 'CZ0sbhZwY290FykPwCE_-1', input_port_name='delta_t')
		self.addConnection('deltaT', 'CZ0sbhZwY290FykPwCE_-6', input_port_name='delta_t')
		self.addConnection('initdxdt', 'CZ0sbhZwY290FykPwCE_-1', input_port_name='IC')
		self.addConnection('x0', 'CZ0sbhZwY290FykPwCE_-6', input_port_name='IC')
		self.addConnection('WgBMcyxID5A1E6gqlP3p-31', 'CZ0sbhZwY290FykPwCE_-1')
		self.addConnection('deltaT', 'kQCSEosvlVg2ZfA-_8SE-22', input_port_name='Din')
		self.addConnection('CZ0sbhZwY290FykPwCE_-6', 'kQCSEosvlVg2ZfA-_8SE-26')
		self.addConnection('kQCSEosvlVg2ZfA-_8SE-22', 'kQCSEosvlVg2ZfA-_8SE-26', output_port_name='sinOut')
		self.addConnection('kQCSEosvlVg2ZfA-_8SE-26', 'kQCSEosvlVg2ZfA-_8SE-32')
		self.addConnection('kQCSEosvlVg2ZfA-_8SE-43', 'kQCSEosvlVg2ZfA-_8SE-36', input_port_name='IC')
		self.addConnection('deltaT', 'kQCSEosvlVg2ZfA-_8SE-36', input_port_name='delta_t')
		self.addConnection('kQCSEosvlVg2ZfA-_8SE-36', 'error')
		self.addConnection('kQCSEosvlVg2ZfA-_8SE-32', 'kQCSEosvlVg2ZfA-_8SE-36')


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
	cbd = CBDB("CBDB", deltaT=0.001)


	# Run the simulation
	cbd.run(20000)

	# process simulation results
	plot_signal(cbd, ['OUT1'], 'Harmonic B')
	plot_signal(cbd, ['error'], 'Error Harmonic B')

