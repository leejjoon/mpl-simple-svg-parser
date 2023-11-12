from mpl_simple_svg_parser import SVGMplPathIterator, get_paths_extents

def main():
    import sys
    import matplotlib.pyplot as plt

    fn = sys.argv[1]
    svg_mpl_path_iterator = SVGMplPathIterator(open(fn).read(), svg2svg=True)
    pc = svg_mpl_path_iterator.get_path_collection()
    b0 = get_paths_extents(pc.get_paths())

    fig, ax = plt.subplots()
    ax.set_aspect(True)
    ax.add_collection(pc)
    ax.set(xlim=(b0.xmin, b0.xmax), ylim=(b0.ymin, b0.ymax))

    plt.show()


if __name__ == '__main__':
    main()
