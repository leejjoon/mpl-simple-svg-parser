import numpy as np
import cairosvg
from mpl_simple_svg_parser import SVGMplPathIterator, get_paths_extents
import io
import matplotlib.image as mpimg

def plot_compare_svg(fig, fn):
    xmlstring = open(fn, "rb").read()
    # xmlstring = open("homer-simpson.svg").read()
    svg_mpl_path_iterator = SVGMplPathIterator(xmlstring, svg2svg=True)

    from matplotlib.gridspec import GridSpec
    gs = GridSpec(1, 3)
    axs = [fig.add_subplot(_) for _ in gs]

    ax = axs[0]
    try:
        png = cairosvg.svg2png(xmlstring)
    except ValueError:
        png = None

    if png is not None:
        arr = mpimg.imread(io.BytesIO(png))
        ax.imshow(arr)

    ax = axs[1]

    ax.set_aspect(True)
    # we first set the viewport
    if svg_mpl_path_iterator.viewbox is not None:
        x1, y1, x2, y2 = svg_mpl_path_iterator.viewbox
        ax.set(xlim=(x1, x2), ylim=(y1, y2))

    ax.transData.transform([[0, 0], [1, 0]])
    px1, px2 = ax.transData.transform([[0, 0], [1, 0]])[:, 0]
    # FIXME : for some reason, width seems to be overestimated by a factor of 0.75
    data_unit_in_points = (px2 - px1) / ax.figure.dpi * 72 * 0.75

    paths = []
    pc = svg_mpl_path_iterator.get_path_collection()
    ax.add_collection(pc)
    # for i in range(len(svg_mpl_path_iterator.groups)):
    #     pc = svg_mpl_path_iterator.get_path_collection(i)
    #     ax.add_collection(pc)
    #     paths.extend(pc.get_paths())

    if svg_mpl_path_iterator.viewbox is None:
        b0 = get_paths_extents(paths)
        ax.set(xlim=(b0.xmin, b0.xmax), ylim=(b0.ymin, b0.ymax))

    pc.set_linewidth(np.array(pc.get_linewidth()) * data_unit_in_points)
    ax.add_collection(pc)

    try:
        svg_mpl_path_iterator = SVGMplPathIterator(xmlstring, svg2svg=True, pico=True)
    except:
        svg_mpl_path_iterator = None

    if svg_mpl_path_iterator is not None:
        ax = axs[2]
        ax.set_aspect(True)
        # we first set the viewport
        if svg_mpl_path_iterator.viewbox is not None:
            x1, y1, x2, y2 = svg_mpl_path_iterator.viewbox
            ax.set(xlim=(x1, x2), ylim=(y1, y2))

        ax.transData.transform([[0, 0], [1, 0]])
        px1, px2 = ax.transData.transform([[0, 0], [1, 0]])[:, 0]
        # FIXME : for some reason, width seems to be overestimated by a factor of 0.75
        data_unit_in_points = (px2 - px1) / ax.figure.dpi * 72 * 0.75

        paths = []
        pc = svg_mpl_path_iterator.get_path_collection()
        ax.add_collection(pc)
        # for i in range(len(svg_mpl_path_iterator.groups)):
        #     pc = svg_mpl_path_iterator.get_path_collection(i)
        #     ax.add_collection(pc)
        #     paths.extend(pc.get_paths())

        if svg_mpl_path_iterator.viewbox is None:
            b0 = get_paths_extents(paths)
            ax.set(xlim=(b0.xmin, b0.xmax), ylim=(b0.ymin, b0.ymax))

        pc.set_linewidth(np.array(pc.get_linewidth()) * data_unit_in_points)
        ax.add_collection(pc)

    return fig


if True:
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    import glob
    from pathlib import Path
    import os.path
    rootdir = Path("w3_svg_samples")
    outdir = Path("w3_svg_samples_out_late_pico")

    for fn in list(rootdir.glob("*.svg"))[:]:
        root, ext = os.path.splitext(os.path.basename(fn))
        print(f"[{root}]")

        # if True:
        try:
            fig = Figure(figsize=(15, 5))
            plot_compare_svg(fig, fn)
            fig.savefig(outdir / f"{root}.png", dpi=130)
        except:
            print("failed")
            continue

# pico late fail
"""
preserve
"""
