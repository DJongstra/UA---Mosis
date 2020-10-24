#
# drawio2cbd.py
#
```
 Copyright the Modelling, Simulation and Design Lab (MSDL)
           http://msdl.cs.mcgill.ca/

 Author(s): Randy Paredis
  
 Purpose: converts an XML file produced using draw.io/diagrams.net
          and the CBDLibrary.xml library of Causal Block Diagram (CBD) blocks
          to a Python source file for use with the CBD simulation framework.

 Requires Python version >= 3.6
 The CBD simulation framework also requires Python version >= 3.6

 Uses the following Python libraries 
  argparse
  re
  zlib
  base64
  xml (for xml.etree.ElementTree) 

 The generated simulator code uses
  bokeh (https://bokeh.org/) for plotting
  Graphviz to display the dependency structure of the CBD
```

## How to use drawio2cbd.py:

### Setting up draw.io (note that the stand-alone executable is drawio)
The script converts an XML file produced using draw.io (or its web-based
incarnation diagrams.net) and the library of Causal Block Diagram (CBD) blocks
CBDLibrary.xml to a Python source file for use with the CBD simulation framework.

In draw.io, select `File > Open Library...` and load `CBDLibrary.xml`.
This provide a set of primitive CBD blocks that can be used in your models. 
You will find it at the top shapes library. 
Note that, as some block labels contain mathematical formulas, these  
are not rendered correctly by default. Rather, you will see labels such as
`\sqrt[y]{x}`. On every page where formula labels are used, enable
`Extras > Mathematical Typesetting`. 

#### Block properties 
All blocks in the library have some block-specific properties that can be set by the user. 
Hovering over a component shows all non-empty properties that were set on this shape.

There are several ways of accessing/modifying these properties:
* Click with right mouse button to open a shape`s context menu. 
  Near the bottom of the list, select `Edit Data...`.
* Select the shape (left mouse button) and in the top of the right panel, 
  go to `Arrange > Edit Data`
* Select the shape and press `CTRL + M`/`CMND+M`.

**Do not change the class_name as the drawio2cbd script relies on this property.**

#### Working with library blocks
To guarantee a consistent visual appearance of CBD models, 
none of the blocks in the library, with the exception of the Custom Block, can be resized. 
Every block has zero or more input and output ports. Input ports are represented by
the `InputPortBlock` (black triangle) and output ports by the `OutputPortBlock`
(white triangle). When selecting (left mouse button) a port, a small, movable, 
yellow/orange diamond-shaped anchor will appear in front of the port`s name. 
The position of this label can be changed by dragging the anchor.
The port name can be altered in the `Edit Data` window.

For each of a CBD model`s top-level `OutputPortBlock`s, a `signal` property
may be added (see above #### Block properties). 
The drawio2cbd will then generate code to produce a plot, using https://bokeh.org/.
Note that bokeh produces an HTML document which is rendered in a browser
and allows some user interaction with the plot.
The value of the `signal` property on a top-level `OutputPortBlock` should be the title 
to be put on the plot. Multiple signals may be rendered onto the same plot.
For more complex CBD simulation result analysis and visualization, code should be added
at the bottom of the generated file.

Each CBD block that is not a port may have the following properties:
* `ID` or `id`: The draw.io unique ID for this block. Note that draw.io automatically
  overwrites a property with the key `id` by the value shown by `ID` (upon saving the diagram).
* `block_name`: The name of the block. The CBD simulator assumes that
  all blocks have a unique name. When omitted, the `ID` is used.
* `class_name`: The type of block. 
  **Do not change the class_name as the drawio2cbd script relies on this property.**
* `symbol`: The block symbol that must be rendered by MathJax/LaTeX. This is a purely
  graphical attribute and is ignored by the script. Is not required for the script to work.

Optionally, additional class parameters can be provided by adding more properties. 
These will be passed on as-is, allowing for complex values. E.g., to
use strings, enclose the value in `"..."` or ``...``. Class parameters that 
cannot be used are: `label` (prevented by draw.io), `id` (overwritten by 
draw.io), `placeholders` (prevented by draw.io), `symbol` (ignored by the script)
and `__docstring__` (used for other purposes, see later).

_Note:_ Blocks with a variable number of inputs (i.e., the `OrBlock` and the 
`AndBlock`) still need additional ports to be placed in the block when calling 
drawio2cbd with the `-p` or `--port` option. Otherwise, one my use a single input, 
as long as the `numberOfInputs` property is set to a value that is at least the total
number of incoming links.

#### Creating your custom blocks
A custom hierarchical CBD block is constructed as a network of already provided blocks 
(which in their own right may be custom hierarchical blocks)
using the `Custom Block` element from `CBDLibrary.xml`. 
This is a collapsible component in which a block diagram may be drawn. 
It has two important properties: 
Property `class_name` is the new class name for the custom block. 
Property `block_name` is the name of an instance of this hierarchical CBD model. 
Additional properties can be added to create custom class parameters. 
The same set of parameters that was discussed above cannot be set, 
with the exception of `__docstring__`, which now allows adding documentation to custom blocks.

The empty rectangle is a container for the custom hierachical block. 
Blocks can be dragged into the rectangular area and connected.
`InputPortBlock` and `OutputPortBlock` are used to add inputs and outputs with 
their `name` property set to the port`s name.

_Hint:_ The `Custom Block` component can, in constrast with all other blocks in the
library, be scaled. This allows for larger hierarchical models to be created, as the 
basic blocks cannot be resized.

Next, create a graphical representation of the block (i.e., what an instance
block should look like when used in a block diagram), add the corresponding 
ports and set the property `class_name` to the same class as that set in the
`Custom Block`. Make sure not to forget to add any class parameters that were
added to the `Custom Block`.

_Hint_: This can be done easily by adding a predefined block and changing its
ports and properties to match the new custom block.

_Note:_ Only the `Custom Block` components will be read by the drawio2cbd script. 
Anything else is implicitly ignored. Furthermore, the script is page-independent,
meaning multiple pages may be used inside a single draw.io document to maintain a 
clean overview of your models. 

### The drawio2cbd script 
The script is to be run with a Python version >= 3.6 as follows:
```
python drawio2cbd.py [options] input [output]
```
Where `input` represents an input file (a saved draw.io diagram, either uncompressed or compressed XML), 
`output` an optional output file name. When omitted, the file will be printed to the console. 
Do note that both must be placed next to one another. `options` is a set of additional
parameters that can influence the converted code:
* `-e ENTRY` or `--entry ENTRY`: The top-level CBD`s name which will be instantiated
  and simulated. Defaults to `Root`.
* `-T DELTA` or `--delta DELTA`: Allows one to change the timestep size. For
  discrete-time CBDs, this should be 1.0. Continuous-time CBD will be 
  be solved in terms of a discrete-time CBD approximation and the stepsize
  will be modelled explicitly as a constant. DELTA defaults to 1.0 (i.e., discrete-time CBDs). 
  This parameter adds a `DELTA_T` variable to the generated simulation code, 
  which may be referenced in draw.io.
* `-t TIME` or `--time TIME`: The simulation stop time. Defaults to `10`.
  Start time is `0`.
* `-d [DRAW]` or `--draw [DRAW]`: The generated code creates `GraphViz`
  representations of certain blocks. When `DRAW` is not given, the top-level block is
  used. Otherwise, `DRAW` is a path to a certain block, with `.` as a path separator.
* `-l [LATEX]` or `--latex [LATEX]`: The generated code prints blocks as a
  `LaTeX`-based set of equations. `LATEX` allows one to identify blocks in the
  same way as was the case for `DRAW` (see above). Note that this option is experimental
  and should not be used. Rather, the simulation framework's LaTeX generation should be 
  implemented and used.
* `-a` or `--all`: When set, CBDs without content will also be created as a class.
  This may be useful for subsequent manual completion of the class.
* `-p` or `--ports`: Some port names can be identified from the context. By
  default, the generated code allows the CBD framework to do so. When this option
  is set, even those ports will explicitly be set.
* `-s SPACES` or `--spaces SPACES`: Allows on to define the number of spaces that should act
  as an indent. When 0 or less, tabs will be used instead. Defaults to `0`.

_Hint:_ Use the `-h` or `--help` flag to get a help menu.

### Running the Simulation
For a simulation to be able to run, Python must be able to locate the CBD simulation framework. 
Once that is taken care of, the generated file can be run as-is. It can also first be
customized with for example specific analysis post-processing of the simulation data. 

_Note:_ The script does not do Python validity checking, so the CBD simulation may
crash upon execution.

## Tips and Tricks
* The script does not care if the file is compressed or not. Yet, for debugging
  purposes and readability, one can disable the compression in the
  `File > Properties...` window in draw.io.
* When the models become quite large, it is possible draw.io starts to lag. 
  This can be prevented by using multiple pages (and sufficient hierarchy).
  Additionally, this makes the overal model file quite clean to work with. The
  conversion script ignores the use of pages and only concerns itself with the
  `Custom Block` components.
* Make sure CBD models are fully contained by the large rectangle in the
  `Custom Block` shape. This can be tested by moving the `Custom Block` shape and
  checking that the contents move as well.
* `Custom Block` shapes can be collapsed by clicking on the grey box in the top
  left corner of the shape.
* `CTRL+D` / `CMND+D` allows one to duplicate shapes.
* Dummy classes can be created by adding an empty block and converting with the
  `-a` or `--all` flag enabled.
* Keep custom shapes as simple as possible. Refrain from using other shapes
  to add icons or graphical representations for blocks. While it will be accepted
  by the script, groups can become quite cumbersome, especially with (partially)
  overlapping shapes. An easier way is by making use of `UTF-8` icons, using
  their `HTML` notation. Take a look at the `TimeBlock` and the `LoggingBlock`
  for an example on how to do this. To add a more complex shape for
  blocks, `Arrange > Insert > Shape...` can be used.

