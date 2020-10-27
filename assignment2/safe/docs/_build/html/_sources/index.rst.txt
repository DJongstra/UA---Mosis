.. Copyright the Modelling, Simulation and Design Lab (MSDL)
      http://msdl.cs.mcgill.ca/

.. drawio2cbd documentation master file, created by
   sphinx-quickstart on Mon Oct 19 12:31:01 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to :code:`drawio2cbd`'s Documentation!
==============================================

The script converts an XML file produced using draw.io (or its web-based
incarnation diagrams.net) and the library of Causal Block Diagram (CBD) blocks
CBDLibrary.xml to a Python source file for use with the CBD simulation framework.

.. note:: In the remainder of this documentation, 'drawio' will be used to refer to draw.io and/or diagrams.net.

.. toctree::
   :maxdepth: 2

:Author: Randy Paredis
:Python Version: >= 3.6
   
   
Installation
------------
In order for :code:`drawio2cbd` to work, and for being able to model CBDs from drawio, the following files
and dependencies are required:

* For :code:`drawio2cbd`:

  * :download:`Drawio CBD Library File <../CBDLibrary.xml>`
  * :download:`drawio2cbd Python Script <../drawio2cbd.py>`
  * *Standard Python Libraries:* :code:`argparse`, :code:`re`, :code:`base64`,
    :code:`zlib`, :code:`xml`, :code:`warnings`, :code:`urllib`

* For Simulation: see `CBD Simulator Development Kit's Documentation <cbd.html>`_

* For Plotting:

  * `matplotlib <https://matplotlib.org>`__
  * `bokeh <https://bokeh.org/>`__ and :code:`itertools`
  * CSV-files can be generated without any additional packages.

   
Setting up Drawio
------------------
In drawio, select :menuselection:`File --> Open Library` and load :file:`CBDLibrary.xml`
(which can be found :download:`here <../CBDLibrary.xml>`).
This provides a set of primitive CBD blocks that can be used in your models. 
Once included, it can be found at the top of the shapes library.

.. figure:: _figures/library.png
   :align: center

   CBD Library in the Sidebar

.. _block-props:

Block Properties
----------------
All blocks in the library have some block-specific properties that can be set by the user. 
Hovering over a component shows all non-empty properties that were set on this shape.

There are several ways of accessing/modifying these properties:

* Click with right mouse button to open a shape's context menu. 
  Near the bottom of the list, select :menuselection:`Edit Data`.
* Select the shape (left mouse button) and in the top of the right panel, 
  go to :menuselection:`Arrange --> Edit Data`.
* Select the shape and press :kbd:`CTRL + M` or :kbd:`CMND + M`.

.. warning:: Do not change the :code:`class_name` as the :code:`drawio2cbd` script relies on this property.

.. figure:: _figures/properties.png
   :align: center
   
   Example of the Property Window (for a ConstantBlock)


.. _library:

Working with Library Blocks
---------------------------
To guarantee a consistent visual appearance of CBD models, 
no blocks in the library, except for the Custom Block, can be resized. 
Every block has zero or more input and output ports. Input ports are represented by
the :code:`InputPortBlock` (black triangle) and output ports by the :code:`OutputPortBlock`
(white triangle). When selecting (left mouse button) a port, a small, movable, 
yellow/orange diamond-shaped anchor will appear in front of the port's name. 
The position of this label can be changed by dragging the anchor.
The port name can be altered in the :menuselection:`Edit Data` window.

For each of a CBD model's top-level :code:`OutputPortBlock` shapes, a :code:`signal` property
may be added (see :ref:`block-props`). 
The :code:`drawio2cbd` will then generate code to produce a plot, using https://bokeh.org/.
Note that bokeh produces an HTML document which is rendered in a browser
and allows some user interaction with the plot.
The value of the :code:`signal` property on a top-level :code:`OutputPortBlock` should be the title 
to be put on the plot. Multiple signals may be rendered onto the same plot.
For more complex CBD simulation result analysis and visualization, code should be added
at the bottom of the generated file.

Each CBD block that is *not* a port may have the following properties:

* :code:`ID` or :code:`id`: The drawio unique ID for this block. Note that drawio automatically
  overwrites a property with the key :code:`id` by the value shown by :code:`ID` (upon saving the diagram).
* :code:`block_name`: The name of the block. It is required that
  all blocks have a unique name within a class. When omitted, the :code:`ID` is used.
* :code:`class_name`: The type of block.

  .. warning:: Do not change the :code:`class_name` as the :code:`drawio2cbd` script relies on this property.
               Changing it makes it so the block type changes as well in the simulation.
  
* :code:`symbol`: The block symbol that must be rendered by MathJax/LaTeX. This is a purely
  graphical attribute and is ignored by the script. Is not required for the script to work.

Optionally, additional class parameters can be provided by adding more properties. 
Their values will be passed on as default values for the corresponding property as an argument, e.g., to
use strings, enclose the value in "..." or '...', for :code:`None`, leave it empty or litterally type
":code:`None`"...

.. warning:: Make sure these values are expressions/rvalues! If not, the generated Python file will crash,
              or cause some unexpected behavior. Furthermore, newlines may not be used in these values.

Class parameters that cannot be used are: :code:`label` (prevented by drawio), :code:`id` (overwritten by 
drawio), :code:`placeholders` (prevented by drawio), :code:`symbol` (ignored by the script)
and :code:`__docstring__` (used for other purposes, see later).

.. note:: Blocks with a variable number of inputs (i.e., the :code:`OrBlock` and the
          :code:`AndBlock`) still need additional ports to be placed in the block when calling 
          :code:`drawio2cbd` with the :code:`-p` or :code:`--port` option. Otherwise, one may use a single input, 
          as long as the :code:`numberOfInputs` property is set to a value that is at least the total
          number of incoming links.


.. _custom-block:

Creating Custom CBD Blocks
-------------------------------
A custom hierarchical CBD block is constructed as a network of already provided blocks 
(which in their own right may be custom hierarchical blocks)
using the :code:`Custom Block` element from :file:`CBDLibrary.xml`. 
This is a collapsible component in which a block diagram may be drawn. 
It has two important properties:

* :code:`class_name`: The new class name for the custom block. Note that all class names must be unique!
* :code:`block_name`: The name of an instance of the CBD model if it's the top-level CBD (see :ref:`script`).

Additional properties can be added to create custom class parameters. 
The same set of parameters that was discussed above cannot be set, 
with the exception of :code:`__docstring__`, which now allows adding documentation to custom blocks.

The empty rectangle is a container for the custom hierachical block. 
Blocks can be dragged into the rectangular area and connected.
:code:`InputPortBlock` and :code:`OutputPortBlock` are used to add inputs and outputs with 
their :code:`name` property set to the port's name.

.. hint:: The :code:`Custom Block` component can, in constrast with all other blocks in the
          library, be resized. This allows for larger hierarchical models to be created, as the 
          basic blocks cannot be resized.

.. figure:: _figures/custom-block.png
   :align: center

   Custom Sine Generator Block with no Input Ports, a single Output Port and a Custom Graphical Representation

Next, create a graphical representation of the block (i.e., what an instance
block should look like when used in a block diagram), add the corresponding 
ports and set the property :code:`class_name` to the same class as that set in the
:code:`Custom Block`. Make sure not to forget to add any class parameters that were
added to the :code:`Custom Block`.

.. hint:: This can be done easily by adding a predefined block and changing its
          ports and properties to match the new custom block.

.. note:: Only the :code:`Custom Block` components will be read by the :code:`drawio2cbd` script. 
          Anything else is implicitly ignored. Furthermore, the script is page-independent,
          meaning multiple pages may be used inside a single drawio document to maintain a 
          clean overview of the created models.

.. _script:

The :code:`drawio2cbd` Script
-----------------------------
The script is to be run with Python (version >= 3.6) as given below. The generated code works with the CBD
simulator, which is also for Python (version >= 3.6).

.. code-block:: bash

   python drawio2cbd.py [options] input [output]

Where :code:`input` represents an input file (a saved drawio diagram, either uncompressed or compressed XML), 
:code:`output` an optional output file name. When omitted, the file will be printed to the console. 
Do note that both must be placed next to one another. :code:`options` is a set of additional
parameters that can influence the converted code:

* :code:`-e ENTRY` or :code:`--entry ENTRY`: The top-level CBD's name which will be instantiated
  and simulated. This option is required.
* :code:`-T DELTA` or :code:`--delta DELTA`: Allows one to change the timestep size. For
  discrete-time CBDs, this should be 1.0. Continuous-time CBD will be 
  be solved in terms of a discrete-time CBD approximation and the stepsize
  will be modelled explicitly as a constant. :code:`DELTA` defaults to 1.0 (i.e., discrete-time CBDs). 
  This parameter adds a :code:`DELTA_T` 'global' variable to the generated simulation code, 
  which may be referenced in drawio.
* :code:`-t TIME` or :code:`--time TIME`: The simulation stop time. Defaults to 10.
  Start time is 0.
* :code:`-P {mpl,matplotlib,bokeh,csv,off,false}` or
  :code:`--plot {mpl,matplotlib,bokeh,csv,off,false}`: Indicates the plotter that can
  be used. :code:`mpl` or :code:`matplotlib` indicates using `matplotlib <https://matplotlib.org>`__,
  :code:`bokeh` will make use of `bokeh <https://bokeh.org>`__, :code:`csv` will write
  the plot data to a CSV file and :code:`off` or :code:`false` indicates no plot
  needs to be created. When the plotting library cannot be found, a warning will be
  shown and the simulation script will still be generated.
* :code:`-a` or :code:`--all`: When set, CBDs without content will also be created as a class.
  This may be useful for subsequent manual completion of the class.
* :code:`-p` or :code:`--ports`: Some port names can be identified from the context. By
  default, the generated code allows the CBD framework to do so. When this option
  is set, even those ports will explicitly be set.
* :code:`-s SPACES` or :code:`--spaces SPACES`: Allows on to define the number of spaces that should act
  as an indent. When 0 or less, tabs will be used instead. Defaults to 0.

.. note:: Use the :code:`-h` or :code:`--help` flag to get a help menu.


Running the Simulation
----------------------
For a simulation to be able to run, Python must be able to locate the CBD simulation framework. 
Once that is taken care of, the generated file can be run as-is. It can also first be
customized with for example specific analysis post-processing of the simulation data. 

.. warning:: The script does not do Python validity checking, so the CBD simulation may
             crash upon execution when the above-mentioned rules are violated (see :ref:`library`
             and :ref:`custom-block`).

Tips and Tricks
---------------

* The script does not care if the file is compressed or not. Yet, for debugging
  purposes and readability, one can disable the compression in the
  :menuselection:`File --> Properties` window in drawio.
* When the models become quite large, it is possible drawio starts to lag. 
  This can be prevented by using multiple pages (and sufficient hierarchy).
  Additionally, this makes the overal model file quite clean to work with. The
  conversion script ignores the use of pages and only concerns itself with the
  :code:`Custom Block` components.
* Make sure CBD models are fully contained by the large rectangle in the
  :code:`Custom Block` shape. This can be tested by moving the :code:`Custom Block` shape and
  checking that the contents move as well. You can see that you're dragging a shape in this
  rectangle if its border becomes a blueish purple.
* :code:`Custom Block` shapes can be collapsed by clicking on the grey box in the top
  left corner of the shape.
* :kbd:`CTRL + D` or :kbd:`CMND + D` allows one to duplicate shapes.
* Dummy classes can be created by adding an empty block and converting with the
  :code:`-a` or :code:`--all` flag enabled. Do note that you would still need to implement
  these classes.
* Keep custom shapes as simple as possible. Refrain from using other shapes
  to add icons or graphical representations for blocks. While it will be accepted
  by the script, groups can become quite cumbersome, especially with (partially)
  overlapping shapes. An easier way is by making use of UTF-8 icons, using
  their HTML notation. Take a look at one of the provided blocks
  for an example on how to do this. To add a more complex shape for
  blocks, :menuselection:`Arrange --> Insert --> Shape` can be used.


