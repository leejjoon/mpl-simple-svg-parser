"""
The svg files are downloaded from https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/
"""
from svg_renderer_helper import compare_svg_result

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
            print(" ----- failed -----")
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
