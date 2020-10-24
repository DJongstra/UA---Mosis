"""This script generates a Python-consistent CBD from an XML file, as
constructed in draw.io / diagrams.net .

:Author: 			Randy Paredis
:Python Version:	3.6+
"""

import xml.etree.ElementTree as ET
import argparse
from urllib.parse import unquote
import zlib
import base64
import re
import warnings

IGNORE = ['id', 'label', 'placeholders', 'symbol', 'class_name', 'block_name', '__docstring__']
"""Properties to ignore when parsing."""

PLOT_FORMATS = ['mpl', 'matplotlib', 'bokeh', 'csv', 'off', 'false']
"""Ways to plot the data."""

class Parser:
	"""Parses a draw.io XML file.

	Args:
		inputfile (str):	Filename for the input.
		outputfile (str):	When a string, this is the output filename.
							When None, the console will be used.
		all_ (bool):		Whether or not to add empty CBD diagrams to the
							generated file.
		ports (bool):		Some port names can be identified from the context.
							By default, the generated code allows the CBD framework
							to do so. When this param is True, even those ports will
							explicitly be set.
	"""
	def __init__(self, inputfile, outputfile=None, all_=False, ports=False):
		self.inputfile = inputfile
		self.outputfile = outputfile
		self.all_ = all_
		self.ports = ports
		self.__block_names = {}
		self.__signals = {}

	@staticmethod
	def decode_and_deflate(data):
		"""Draw.io compresses each page as follows:
		First, all data is url-encoded
		Next, it is compressed/deflated
		Finally, it is encoded according to base64.

		To obtain the page data, we have to do the reverse.

		Returns:
			Uncompressed and decoded data as a string.
		"""
		decoded_data = base64.b64decode(data)
		inflated = zlib.decompress(decoded_data, -15).decode('utf-8')
		url_decoded_data = unquote(inflated)
		return ET.fromstring(url_decoded_data)
		
	def parse(self):
		"""Does the actual file parsing.

		If the file is compressed, we uncompress and work from there.
		If it wasn't compressed, we can work with the whole tree.

		Only looks at "Custom Class" shapes that have a "class_name"
		set.

		Returns:
		 	An iterator of all classes that must be generated.
		"""
		tree = ET.parse(self.inputfile)
		root = tree.getroot()
		compressed = len(root.findall(".//mxGraphModel")) == 0
		if compressed:
			# If compressed, first decode base64, then deflate, then url decode
			pages = root.findall(".//diagram")
			for page in pages: # Decoding happens pagewise
				nroot = self.decode_and_deflate(page.text)
				objects = nroot.findall(".//object/mxCell/mxGeometry/mxRectangle/../../..[@class_name]")
				for obj in objects:
					yield self.create_class(nroot, **obj.attrib)
		else:
			objects = root.findall(".//object/mxCell/mxGeometry/mxRectangle/../../..[@class_name]")
			for obj in objects:
				yield self.create_class(root, **obj.attrib)
			
	def create_class(self, root, class_name, **kwargs):
		"""Creates a class.

		Args:
			root:				The root element for this class. Must be the document.
								Is used to find links with other classes.
			class_name (str):	The name for the class.
			**kwargs:			Additional class parameters as set in the Properties window.

		Returns:
		 	A class as a string.
		"""
		if class_name in self.__block_names:
			raise ParseException(f"Class '{class_name}' already defined.")
		if re.search(r"\s", class_name) is not None:
			raise ParseException(f"In class '{class_name}': Class names may not contain spaces.")
		self.__block_names[class_name] = kwargs.get("block_name", class_name)
		if self.__block_names[class_name] is None or self.__block_names[class_name] == "":
			self.__block_names[class_name] = class_name
		rect = root.findall(".//*[@parent='%s']" % kwargs["id"])[1]
		components = root.findall(".//object/mxCell[@parent='%s']/.." % rect.attrib["id"])
		inputs = []
		outputs = []
		blocks = []
		lookup = {}
		__added = []
		for com in components:
			att = com.attrib
			if att["class_name"] == "InputPortBlock":
				inputs.append(att["name"])
				lookup[att["id"]] = att["name"]
			elif att["class_name"] == "OutputPortBlock":
				outputs.append(att["name"])
				lookup[att["id"]] = att["name"]
				if "signal" in att and att["signal"] != "":
					self.__signals.setdefault(class_name, {}).setdefault(att["signal"], []).append(att["name"])
			else:
				block_name = att.get("block_name", att["id"])
				if block_name == '':
					block_name = att['id']
				if block_name in __added:
					raise ParseException(f"In class '{class_name}': Block with name '{block_name}' already exists.")
				__added.append(block_name)
				lookup[att["id"]] = block_name
				if any(["\n" in v for v in att.values()]):
					raise ParseException(f"In class '{class_name}', block '{block_name}' ({att['class_name']}): Block properties should not contain newlines!")
				blocks.append("self.addBlock(%s(%s))" % (att["class_name"],
					", ".join(["block_name='%s'" % block_name] + \
							  [f"{k}=({v.strip() if v != '' else None})" for k, v in att.items() if k not in IGNORE])))
		blocks = f"\n{TABS}{TABS}".join(blocks)
			
		edges = root.findall(".//*[@parent='%s'][@edge='1']" % rect.attrib["id"])
		connections = []
		for edge in edges:
			att = edge.attrib
			source = root.find(".//*[@id='%s']" % att["source"])
			target = root.find(".//*[@id='%s']" % att["target"])
			if source.attrib["class_name"] == "InputPortBlock":
				sblock = source.attrib["name"]
				ipn = ""
			else:
				sblock = lookup[source[0].attrib["parent"]]
				if not self.ports and source.attrib["name"] == "OUT1":
					ipn = ""
				else:
					ipn = source.attrib["name"]
			if target.attrib["class_name"] == "OutputPortBlock":
				tblock = target.attrib["name"]
				opn = ""
			else:
				tblock = lookup[target[0].attrib["parent"]]
				if not self.ports and re.match(r"IN\d+", target.attrib["name"]):
					opn = ""
				else:
					opn = target.attrib["name"]
			conn = "self.addConnection('%s', '%s'" % (sblock, tblock)
			if opn != "":
				conn += ", input_port_name='%s'" % opn
			if ipn != "":
				conn += ", output_port_name='%s'" % ipn
			conn += ")"
			connections.append(conn)
		connections = f"\n{TABS}{TABS}".join(connections)

		if not self.all_ and connections == "" and blocks == "":
			return ""

		docstring = kwargs.get("__docstring__", "")
		if docstring != "":
			docstring = f'\n{TABS}"""{docstring}"""'
		if any(["\n" in v for v in kwargs.values()]):
			raise ParseException(f"In class '{class_name}': Properties should not contain newlines!")
		kv = ", ".join([""] + [f"{k}=({v.strip() if v != '' else None})" for k, v in kwargs.items() if k not in IGNORE])
		return f"""
class {class_name}(CBD):{docstring}
{TABS}def __init__(self, block_name{kv}):
{TABS}{TABS}CBD.__init__(self, block_name, input_ports={inputs}, output_ports={outputs})
		
{TABS}{TABS}# Create the blocks
{TABS}{TABS}{blocks}
		
{TABS}{TABS}# Connect the blocks
{TABS}{TABS}{connections}
"""

	def create_file(self, command, entry='main', delta=None, time=10, draw=None, latex=None, plot=None):
		"""Creates the full file.

		Args:
			command (str):	The command that was used to run this script.
			entry (str):	The main class entry point.
			delta (float):	The timestep size. This is 1 for Discrete-Time CBDs.
			time (int):		How long the simulation should run.
			draw:			List of blocks to draw. None indicates the empty list.
			latex:			List of blocks to generate LaTeX for. None indicates the empty list.
			plot (str):		The plotting format to use. None indicates no plotting.

		Returns:
		 	The file as a string.
		"""
		# Check which blocks to draw
		draw_import = ""
		draw_func = ""
		if draw is not None:
			draw_import = "\nfrom CBDMultipleOutput.Source.CBDDraw import draw"
			if len(draw) > 1:
				draw_func = f"""
{TABS}# Draw the CBDs
{TABS}for to_draw in {draw}:
{TABS}{TABS}block, path = get_block(cbd, to_draw)
{TABS}{TABS}draw(block, '%s.gv' % path)"""
			else:
				if draw[0] == '':
					draw_func = f"\n{TABS}# Draw the CBD\n{TABS}draw(cbd, '%s.gv' % cbd.getBlockName())"
				else:
					draw_func = f"\n{TABS}# Draw the CBD\n{TABS}draw(get_block(cbd, '{draw[0]}')[0], '{draw[0]}.gv')"

		# Check which blocks to generate LaTeX for
		latex_func = ""
		if latex is not None:
			if len(latex) > 1:
				latex_func = f"""

{TABS}# Print the CBDs as LaTeX
{TABS}for to_tex in {latex}:
{TABS}{TABS}block, path = get_block(cbd, to_tex)
{TABS}{TABS}print("LaTeX for '%s':" % path)
{TABS}{TABS}print(block.latex(), '\\n')"""
			else:
				if latex[0] == '':
					latex_func = f"""

{TABS}# Print the CBD as LaTeX
{TABS}print("LaTeX for '%s':" % cbd.getBlockName())
{TABS}print(cbd.latex(), '\\n')"""
				else:
					latex_func = f"""

{TABS}# Print the CBD as LaTeX
{TABS}print("LaTeX for '{latex[0]}':")
{TABS}print(get_block(cbd, '{latex[0]}')[0].latex(), '\\n')"""

		# Actual class creation
		cls = "\n".join(self.parse())

		# Signal info
		signals = f"\n{TABS}# TODO: process your results"
		sig_fnc = ""
		if plot is not None and plot not in ['off', 'false']:
			if entry in self.__signals:
				signals = ""
				for title, sgs in self.__signals[entry].items():
					signals += f"\n{TABS}plot_signals(cbd, {sgs}, '{title}')"
				sig_fnc = self.signal(plot, delta is not None)

		# Set times:
		_delta = ""
		run = f"cbd.run({time})"
		if delta is not None:
			_delta = f"{TABS}DELTA_T = {delta}\n\n"
			run = f"cbd.run({time}, delta_t=DELTA_T)"

		# Actual file construction
		return f"""#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   {command}

from CBDMultipleOutput.Source.CBD import *{draw_import}
{sig_fnc}

def get_block(block, path=""):
{TABS}if path == '': return block, block.getBlockName()
{TABS}cur = block
{TABS}for p in path.split('.'):
{TABS}{TABS}cur = cur.getBlockByName(p)
{TABS}return cur, path

{cls}

if __name__ == '__main__':
{_delta}{TABS}cbd = {entry}("{self.__block_names.get(entry, 'root')}")
{draw_func}{latex_func}

{TABS}# Run the simulation
{TABS}{run}

{TABS}# process simulation results{signals}
"""

	@staticmethod
	def signal(format:str, ct=False):
		"""Creates a draw_signals function and corresponing imports, based on
		the given format. Accepted formats are 'matplotlib' (or 'mpl' for short),
		'bokeh' and 'csv'.

		Args:
			format (str):	How the signal must be outputted.
							Can be one of ['matplotlib', 'mpl', 'bokeh', 'csv']
			ct (bool): 		Whether or not the plot indicates a continuous-time
							simulation. When it does, a line-plot will be used
							for the plots, otherwise a dotted plot is used. For
							CSV and XML this attribute has no effect.
							Defaults to 'False'.

		Returns:
			A string, including a 'plot_signal' function for the generated file.
		"""
		assert format in PLOT_FORMATS
		imports = ""
		plot = ""

		if format in ['matplotlib', 'mpl']:
			imports = """
import matplotlib.pyplot as plt
"""
			plot = f"""
{TABS}plt.figure()
{TABS}plt.title(title)
{TABS}plt.xlabel('time')
{TABS}plt.ylabel('N')
{TABS}for i in range(len(signals)):
{TABS}{TABS}plt.{'plot' if ct else 'scatter'}(times, outputs[i], label=signals[i])
{TABS}plt.legend()
{TABS}plt.show()
"""

		elif format == 'bokeh':
			imports = """
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Dark2_5 as palette
import itertools
"""
			plot = f"""
{TABS}colors = itertools.cycle(palette) 
{TABS}output_file("%s.html" % title.replace(' ', '_').lower(), title=title)
{TABS}p = figure(title=title, x_axis_label='time', y_axis_label='N')
{TABS}for i in range(len(signals)):
{TABS}{TABS}p.{'line' if ct else 'circle'}(x=times, y=outputs[i], legend_label=signals[i], color=next(colors))
{TABS}show(p)
"""

		elif format == 'csv':
			plot = f"""
{TABS}with open("%s.csv" % title.replace(' ', '_').lower(), 'w') as file:
{TABS}{TABS}file.write('time, %s' % ', '.join(signals))
{TABS}{TABS}for i in range(len(times)):
{TABS}{TABS}{TABS}file.write(f'\\n{{times[i]}}, %s' % ', '.join([str(o[i]) for o in outputs]))
"""
		try:
			exec(imports)
		except ImportError as e:
			warnings.warn(f"Cannot find plotting framework '{format}' ({str(e)}); use one of {PLOT_FORMATS}.", UserWarning)

		return f"""
{imports}

def plot_signals(block, signals, title):
{TABS}times = []
{TABS}outputs = []

{TABS}for signal in signals:
{TABS}{TABS}tvpl = block.getSignal(signal)
{TABS}{TABS}times = [t for t, _ in tvpl]
{TABS}{TABS}outputs.append([v for _, v in tvpl])

{TABS}# Plot{plot}
"""

	def convert(self, command, entry='main', delta=None, time=10, draw=None, latex=None, plot=None):
		"""Does the conversion and creates a file or prints to the console.

		Args:
			command (str):	The command that was used to run this script.
			entry (str):	The main class entry point.
			delta (float):	The timestep size. This is 1 for Discrete-Time CBDs.
			time (int):		How long the simulation should run.
			draw:			List of blocks to draw. None indicates the empty list.
			latex:			List of blocks to generate LaTeX for. None indicates the empty list.
			plot (str):		The plotting format to use. None indicates no plotting.
		"""
		contents = self.create_file(command, entry, delta, time, draw, latex, plot)
		if self.outputfile is None:
			print(contents)
		else:
			with open(self.outputfile, 'w') as file:
				file.write(contents)


class ParseException(Exception):
	"""Semantic exceptions when parsing."""
	def __init__(self, message):
		super().__init__(message)

if __name__ == '__main__':
	from sys import argv

	argprs = argparse.ArgumentParser(description='Create Python3 CBD simulations from draw.io/diagrams.net XML files.')
	argprs.add_argument('input', type=str,
						help="the input file to convert")
	argprs.add_argument('output', type=str, default=None, nargs='?',
						help="an optional output file; when omitted, it will be printed to the console")
	argprs.add_argument("-e", "--entry", required=True,
						help="the main CBD to use as a simulation entrypoint")
	argprs.add_argument("-T", "--delta", default=None, type=float,
						help="timestep of the simulation; used for continuous-time CBDs (default: 1.0)")
	argprs.add_argument("-t", "--time", default=10, type=int,
						help="total simulation time steps to take (default: 10)")
	# argprs.add_argument("-d", "--draw", action='append', nargs='?', const='',
	# 					help="makes it so the script draws a Graphviz model for the given CBD path "
	# 						 "(use '.' as path separator)")
	# argprs.add_argument("-l", "--latex", action='append', nargs='?', const='',
	# 					help="outputs LaTeX code for the block (use '.' as path separator)")
	argprs.add_argument('-P', '--plot', choices=PLOT_FORMATS, default='mpl',
						help="sets plotter to use in generated script")
	argprs.add_argument('-a', '--all', action='store_true',
						help="when set, empty CBDs will be created as a class, otherwise they are ignored")
	argprs.add_argument('-p', '--ports', action='store_true',
						help="when set, even the default ports will be explicitly set")
	argprs.add_argument('-s', '--spaces', type=int, default=0,
						help="when set larger than 0, this amount of spaces will be used instead of tabs (default: 0)")
	args = argprs.parse_args()
	TABS = "\t"
	if args.spaces > 0:
		TABS = " " * args.spaces
	parser = Parser(args.input, args.output, args.all, args.ports)
	parser.convert(" ".join(argv), args.entry, args.delta, args.time, None, None, args.plot)
	

