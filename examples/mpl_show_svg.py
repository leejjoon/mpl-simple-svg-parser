import numpy as np
import cairosvg
import argparse
from mpl_simple_svg_parser import SVGMplPathIterator, get_paths_extents
import io
import matplotlib.image as mpimg

def main():
    import sys
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser(
                        prog='mpl show svg')
    parser.add_argument('filename')
    parser.add_argument('-c', '--compare', action='store_true')
    args = parser.parse_args()

    xmlstring = open(args.filename).read()
    # xmlstring = open("homer-simpson.svg").read()
    svg_mpl_path_iterator = SVGMplPathIterator(xmlstring, svg2svg=True)

    if args.compare:
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))

        try:
            png = cairosvg.svg2png(xmlstring)
        except ValueError:
            png = None

        if png is not None:
            arr = mpimg.imread(io.BytesIO(png))
            axs[0].imshow(arr)

        ax = axs[1]
        # ax.set_aspect(True)
        # ax.add_collection(pc)
        # ax.set(xlim=(b0.xmin, b0.xmax), ylim=(b0.ymin, b0.ymax))

    else:
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))

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
    pc = svg_mpl_path_iterator.get_path_collection(None)
    ax.add_collection(pc)
    for i in range(len(svg_mpl_path_iterator.groups)):
        pc = svg_mpl_path_iterator.get_path_collection(i)
        ax.add_collection(pc)
        paths.extend(pc.get_paths())

    if svg_mpl_path_iterator.viewbox is None:
        b0 = get_paths_extents(paths)
        ax.set(xlim=(b0.xmin, b0.xmax), ylim=(b0.ymin, b0.ymax))

    pc.set_linewidth(np.array(pc.get_linewidth()) * data_unit_in_points)
    ax.add_collection(pc)

    plt.show()


if __name__ == '__main__':
    main()
