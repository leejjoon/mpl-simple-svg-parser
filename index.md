---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: archive

gallery:
  - alt: rendering of python.svg
    image_path: /assets/images/python.png
    title: python
    url: /assets/images/python.png

---

# SVG rendering Samples w/ mpl-simple-svg-parser

This sample result page for *mpl-simple-svg-parser*, which try to read the svg
file as a vector path for Matplotlib. It utilizes
[cairosvg](https://cairosvg.org/) and
[picosvg](https://github.com/googlefonts/picosvg) to convert the input svg to
more manageable svg, and read it using
[svgpath2mpl](https://github.com/nvictus/svgpath2mpl) and some custom code.

It is meant to be good enough, not 100% compatible.

Here is an example comparing the rendered results between inkscape, cairosvg and
mpl-simple-svg-parser. The two on the right are rendered by matplotlib (with
different options). And yes, we do support gradient while inefficient
(indirectly using cairosvg).

{% include gallery caption="Python in svg" %}

Take a look at the [sample gallery](gallery) to see how good/bad it is.
