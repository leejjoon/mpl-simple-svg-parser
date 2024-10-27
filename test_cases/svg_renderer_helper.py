"""Helper class to render svg with different renderer (inkscape, cairosvg, mpl-simple-svg-parser) in matplotlib.
"""

import numpy as np
import cairosvg
import io
import matplotlib.image as mpimg
from matplotlib.gridspec import GridSpec
import subprocess

from mpl_simple_svg_parser import SVGMplPathIterator
from mpl_simple_svg_parser.svg_helper import draw_svg

class RunInkscape:
    def __init__(self, inkscape_path="inkscape"):
        self.inkscape_path = inkscape_path

    def get_arr(self, svg_bytes):
        result = subprocess.run([self.inkscape_path,
                                 '--export-type=png', '--export-filename=-',
                                 '--pipe'],
                                input=svg_bytes,
                                capture_output=True)

        arr = mpimg.imread(io.BytesIO(result.stdout))
        return arr


def show_inkscape(ax, xmlbyte):
    ax.set_aspect(True)
    ax.set_title("inkscape")

    arr = RunInkscape().get_arr(xmlbyte)
    ax.imshow(arr)


def show_cairosvg(ax, xmlbyte):
    ax.set_aspect(True)
    ax.set_title("cairosvg")

    try:
        png = cairosvg.svg2png(xmlbyte)
    except ValueError:
        png = None

    if png is None:
        return

    arr = mpimg.imread(io.BytesIO(png))
    ax.imshow(arr)


def show_svg2svg(ax, xmlbyte):
    ax.set_aspect(True)
    ax.set_title("MPL:svg2svg")

    svg_mpl_path_iterator = SVGMplPathIterator(xmlbyte, svg2svg=True)
    open("cairo.svg", "wb").write(svg_mpl_path_iterator.xmlstring)

    draw_svg(ax, svg_mpl_path_iterator)

    x1, y1, w, h = svg_mpl_path_iterator.viewbox
    ax.set(xlim=(x1, x1+w), ylim=(y1, y1+h))


def show_pico(ax, xmlbyte):
    ax.set_aspect(True)
    ax.set_title("MPL:svg2svg+pico")

    try:
        svg_mpl_path_iterator = SVGMplPathIterator(xmlbyte, svg2svg=True, pico=True)
    except:
        svg_mpl_path_iterator = None
    open("pico.svg", "wb").write(svg_mpl_path_iterator.xmlstring)

    if svg_mpl_path_iterator is None:
        return

    draw_svg(ax, svg_mpl_path_iterator)

    x1, y1, w, h = svg_mpl_path_iterator.viewbox
    ax.set(xlim=(x1, x1+w), ylim=(y1, y1+h))


def compare_svg_result(fig, fn):
    xmlbyte = open(fn, "rb").read()

    # xmlstring = open("homer-simpson.svg").read()

    gs = GridSpec(1, 4)
    axs = [fig.add_subplot(_) for _ in gs]

    for ax in axs:
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        for sp in ax.spines.values(): sp.set_visible(False)

    show_inkscape(axs[0], xmlbyte)

    show_cairosvg(axs[1], xmlbyte)

    show_svg2svg(axs[2], xmlbyte)

    show_pico(axs[3], xmlbyte)

    return fig
