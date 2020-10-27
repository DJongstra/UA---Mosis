#
# CBD Simulator Framework 
#
```
 Copyright the Modelling, Simulation and Design Lab (MSDL)
           http://msdl.cs.mcgill.ca/

 Author(s): Marc Provost
            Hans Vangheluwe
            Joachim Denil
            Claudio Gomes
            Randy Paredis
  
 Purpose: converts an XML file produced using draw.io/diagrams.net
          and the CBDLibrary.xml library of Causal Block Diagram (CBD) blocks
          to a Python source file for use with the CBD simulation framework.

 Requires Python version >= 3.6

 Uses the following Python libraries 
  unittest
  math 
  collections (for collections.namedtuple)
  os
  sys
  datetime
  bokeh (https://bokeh.org/) for plotting
  Graphviz to display the dependency structure of the CBD
```

## How to use the Simulator Framework:

### Prerequisites

For plotting, the code uses the Bokeh library. 
To install bokeh for Python, if it is not already installed, follow the instructions
 in: <https://bokeh.pydata.org/en/latest/docs/user_guide/quickstart.html#installation>

To display dependencies between CBD blocks, the Graphviz library is used.
To install Graphviz, if it is not already, follow the steps:
1. Download and install Graphviz: <https://www.graphviz.org/download/>
1. Make sure the Graphviz binaries are accessible in the PATH environment variable. For example, on
 windows there should be an entry in the PATH with: `C:\Graphviz2.38\bin`
1. Install graphviz for python: <https://graphviz.readthedocs.io/en/stable/manual.html>
   1. Note: for anaconda users, use <https://anaconda.org/anaconda/graphviz>

### Running the tests

From the root directory of the CBD Simulator Framework (i.e., where this README file resides).
```
python -m unittest discover -v CBDMultipleOutput.Test "*.py"
```

testDerivatorBlock and testIntegratorBlock will fail while working on the Discrete-Time CBD simulator.

### Running examples 

Make sure that PYTHONPATH includes the root directory of the CBD Simulator Framework.
 
```
cd examples/EvenNumberGen/
python EvenNumberGen.py
```

```
cd examples/Fibonacci/
python Fibonacci.py
```

Both will generate an HTML document containing a bokeh plot in the current directory.

