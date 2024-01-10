Welcome to mpl_simple_svg_parser's documentation!
===================================================================

A simple SVG parser for matplotlib. It read the svg file as a vector path for
Matplotlib.
It utilizes
[cairosvg](https://cairosvg.org/) and
[picosvg](https://github.com/googlefonts/picosvg) to convert the input svg to
more manageable svg, and read it using
[svgpath2mpl](https://github.com/nvictus/svgpath2mpl) and some custom code.

It is meant to be good enough, not 100% compatible. We support gradient, but no filtes etc.

If you are interested, please check out the [sample
page](https://leejjoon.github.io/mpl-simple-svg-parser/gallery/), were we
compare the rendering result of mpl-simple-svg-parser to to other renderer,
including Inkscape.


Installation
^^^^^^^^^^^^^

.. code-block:: bash

   pip install mpl_simple_svg_parser

Getting Help
^^^^^^^^^^^^


.. toctree::
   :maxdepth: 3

   examples/index
   API
   Contributing



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
