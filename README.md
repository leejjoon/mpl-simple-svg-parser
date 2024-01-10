# mpl-simple-svg-parser

A simple SVG parser for matplotlib. It read the svg file as a vector path for
Matplotlib. It utilizes cairosvg and picosvg to convert the input svg to more
manageable svg, and read it using svgpath2mpl.

It is meant to be good enough, not 100% compatible. We support gradient, but no filtes etc.

Please check out the [sample
page](https://leejjoon.github.io/mpl-simple-svg-parser/gallery/), were we
compare the rendering result of mpl-simple-svg-parser to to other renderer,
including inkscape.

## Installation

You can install using `pip`:

```bash
pip install mpl_simple_svg_parser
```

## Development Installation


```bash
pip install -e ".[dev]"
```

