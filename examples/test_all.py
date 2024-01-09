"""
The svg files are downloaded from https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/
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
    # ax.axis("off")

    arr = RunInkscape().get_arr(xmlbyte)
    ax.imshow(arr)
    # offsetbox = OffsetImage(arr)

    # ab = AnnotationBbox(offsetbox, (0.5, 0.5), box_alignment=(0.5, 0.5),
    #                     xycoords='data')
    # ax.add_artist(ab)



def show_cairosvg(ax, xmlbyte):
    ax.set_aspect(True)
    ax.set_title("cairosvg")
    # ax.axis("off")

    try:
        png = cairosvg.svg2png(xmlbyte)
    except ValueError:
        png = None

    if png is None:
        return

    arr = mpimg.imread(io.BytesIO(png))

    ax.imshow(arr)
    # offsetbox = OffsetImage(arr)

    # ab = AnnotationBbox(offsetbox, (0.5, 0.5), box_alignment=(0.5, 0.5),
    #                     xycoords='data')
    # ax.add_artist(ab)



def show_svg2svg(ax, xmlbyte):
    ax.set_aspect(True)
    # ax.axis("off")
    ax.set_title("MPL:svg2svg")

    svg_mpl_path_iterator = SVGMplPathIterator(xmlbyte, svg2svg=True)

    draw_svg(ax, ax, ax.transData, svg_mpl_path_iterator)

    x1, y1, w, h = svg_mpl_path_iterator.viewbox
    ax.set(xlim=(x1, x1+w), ylim=(y1, y1+h))
    # offsetbox = get_svg_drawing_area(ax, svg_mpl_path_iterator)

    # ab = AnnotationBbox(offsetbox, (0.5, 0.5), box_alignment=(0.5, 0.5),
    #                     xycoords='data')
    # ax.add_artist(ab)



def show_pico(ax, xmlbyte):
    ax.set_aspect(True)
    # ax.axis("off")
    ax.set_title("MPL:svg2svg+pico")

    try:
        svg_mpl_path_iterator = SVGMplPathIterator(xmlbyte, svg2svg=True, pico=True)
    except:
        svg_mpl_path_iterator = None

    if svg_mpl_path_iterator is None:
        return

    draw_svg(ax, ax, ax.transData, svg_mpl_path_iterator)

    x1, y1, w, h = svg_mpl_path_iterator.viewbox
    ax.set(xlim=(x1, x1+w), ylim=(y1, y1+h))

    # offsetbox = get_svg_drawing_area(ax, svg_mpl_path_iterator)

    # ab = AnnotationBbox(offsetbox, (0.5, 0.5), box_alignment=(0.5, 0.5),
    #                     xycoords='data')
    # ax.add_artist(ab)


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

if False:
    import matplotlib.pyplot as plt
    fig = plt.figure(1, figsize=(8, 2.3))
    fig.clf()
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.05, hspace=0.05, wspace=0.05)
    fig.patch.set_fc("gold")

    fn = "w3_svg_samples/smile.svg"
    compare_svg_result(fig, fn)
    plt.show()


if True:
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    import glob
    from pathlib import Path
    import os.path
    import toml

    rootdir = Path("w3_svg_samples")
    outdir = Path("w3_svg_samples_out_late_pico")

    svglist = []
    for fn in list(sorted(rootdir.glob("*.svg")))[5:]:
        root, ext = os.path.splitext(os.path.basename(fn))
        print(f"[{root}]")

        fig = plt.figure(1, figsize=(8, 2.3))
        fig.clf()
        fig.subplots_adjust(left=0.01, right=0.99, bottom=0.05, hspace=0.05, wspace=0.05)
        fig.patch.set_fc("gold")

        # if True:
        try:
            compare_svg_result(fig, fn)
            fig.savefig(outdir / f"{root}.png", dpi=130)
            svglist.append((root, True))
        except:
            print("failed")
            svglist.append((root, False))

    from collections import OrderedDict
    # svgs = OrderedDict()
    svgs = []
    import yaml
    for root, png_success in svglist:
        svgname = f"{root}.svg"
        pngname = f"{root}.png" if png_success else ""

        # svgs[root] = {"svgname": svgname, "pngname": pngname}
        svgs.append({"url": f"/assets/images/{root}.png",
                     "image_path": f"/assets/images/{root}.png",
                     "alt": f"rendering of {root}.svg",
                     "title": f"{root}"})

    yaml.dump(svgs, open("mpl-svg-test-w3c.yaml", "w"))

# pico late fail
"""
preserve
"""
