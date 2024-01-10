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

    # xmlstring = open(args.filename).read()
    b_xmlstring = open(args.filename, "rb").read()
    # xmlstring = open("homer-simpson.svg").read()

    if args.compare:
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))

        try:
            png = cairosvg.svg2png(b_xmlstring)
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

    svg_mpl_path_iterator = SVGMplPathIterator(b_xmlstring, svg2svg=True)
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

    svg_mpl_path_iterator = SVGMplPathIterator(b_xmlstring, svg2svg=True, pico=True)
    # try:
    #     svg_mpl_path_iterator = SVGMplPathIterator(b_xmlstring, svg2svg=True, pico=True)
    # except:
    #     svg_mpl_path_iterator = None

    if svg_mpl_path_iterator is not None:
        ax = axs[2]
        ax.set_aspect(True)
        # we first set the viewport
        if svg_mpl_path_iterator.viewbox is not None:
            x1, y1, x2, y2 = svg_mpl_path_iterator.viewbox
            ax.set(xlim=(x1, x2), ylim=(y1, y2))

        paths = []
        pc = svg_mpl_path_iterator.get_path_collection()
        # ax.add_collection(pc)
        # for i in range(len(svg_mpl_path_iterator.groups)):
        #     pc = svg_mpl_path_iterator.get_path_collection(i)
        #     ax.add_collection(pc)
        #     paths.extend(pc.get_paths())

        # open("t.svg", "w").write(svg_mpl_path_iterator.xmlstring)
        if svg_mpl_path_iterator.viewbox is None:
            b0 = get_paths_extents(paths)
            ax.set(xlim=(b0.xmin, b0.xmax), ylim=(b0.ymin, b0.ymax))

        ax.transData.transform([[0, 0], [1, 0]])
        px1, px2 = ax.transData.transform([[0, 0], [1, 0]])[:, 0]
        # FIXME : for some reason, width seems to be overestimated by a factor of 0.75
        data_unit_in_points = (px2 - px1) / ax.figure.dpi * 72 * 0.75

        pc.set_linewidth(np.array(pc.get_linewidth()) * data_unit_in_points)
        ax.add_collection(pc)


    plt.show()


if __name__ == '__main__':
    main()
