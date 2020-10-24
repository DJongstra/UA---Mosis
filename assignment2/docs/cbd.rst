.. Copyright the Modelling, Simulation and Design Lab (MSDL)
      http://msdl.cs.mcgill.ca/

CBD Simulator Development Kit
=============================

Python-based framework for CBD modeling and simulation.

.. toctree::
   :maxdepth: 2

:Authors:
  * Marc Provost
  * Hans Vangheluwe
  * Joachim Denil
  * Claudio Gomes
  * Randy Paredis

:Python Version: >= 3.6
   
   
Prerequisites
-------------
The following packages are required to run simulations using this framework:

* *Standard Python Modules:* :code:`unittest`, :code:`math`, :code:`collections` (for :code:`collections.namedtuple`),
  :code:`os`, :code:`sys`, :code:`datetime`
* `bokeh <https://bokeh.org>`_ for plotting. To install bokeh for python, follow
  `these instructions <https://bokeh.pydata.org/en/latest/docs/user_guide/quickstart.html#installation>`_.
* `GraphViz <http://graphviz.org/>`_ to display the dependency structure of the CBD. To install Graphviz,
  follow these steps:

  1. Download and install Graphviz: https://www.graphviz.org/download/
  2. Make sure the Graphviz binaries are accessible in the PATH environment variable.
     For example, on windows there should be an entry in the PATH with: :file:`C:\\Graphviz2.38\\bin`
  3. Install :code:`graphviz` for Python: https://graphviz.readthedocs.io/en/stable/manual.html

    .. note:: For anaconda users, use https://anaconda.org/anaconda/graphviz


Running the Tests
-----------------
From the root directory of the CBD Simulator Framework (i.e., where this README file resides), execute:

.. code-block:: bash

    python -m unittest discover -v CBDMultipleOutput.Test "*.py"

:code:`testDerivatorBlock` and :code:`testIntegratorBlock` will fail while working on the Discrete-Time CBD simulator.


Running Examples
----------------
Make sure that PYTHONPATH includes the root directory of the CBD Simulator Framework.

.. code-block:: bash

    cd examples/EvenNumberGen/
    python EvenNumberGen.py

.. code-block:: bash

    cd examples/Fibonacci/
    python Fibonacci.py

Both will generate an HTML document containing a bokeh plot in the current directory.
