from matplotlib.patches import PathPatch
from mpl_simple_svg_parser.svg_mpl_path_iterator import SVGMplPathIterator
from mpl_simple_svg_parser.svg_gradient_hlper import GradientHelper

# fn = "w3_svg_samples/car.svg"
fn = "w3_svg_samples/python.svg"
# fn = "sphere.svg"
b_xmlstring = open(fn, "rb").read()
# b_xmlstring = xmlstring.encode("ascii")
s = SVGMplPathIterator(b_xmlstring, pico=True)
u = s.xmlstring

# gradient = ET.fromstring(gradient_string)
box = s.viewbox

gh = GradientHelper(s)
gradient_dict = gh.get_all()

import matplotlib.pyplot as plt
fig, ax = plt.subplots(num=1, clear=True)
ax.set_aspect(1)

vv = list(s.iter_mpl_path_patch_prop())

import mpl_visual_context.patheffects as pe
from mpl_visual_context.image_box import ImageBox

for p1, d in vv:
    p = PathPatch(p1, ec=d["ec"], fc=d["fc"], alpha=d["alpha"])
    ax.add_patch(p)
    # print(d)

    import re
    p_url = re.compile(r"url\(#(.+)\)")

    if (fc_orig := d.get("fc_orig")) and (m := p_url.match(fc_orig)):
        gradient_name = m.group(1)
        arr = gradient_dict[gradient_name]
        image_bbox = ImageBox(
            arr[::-1],
            # coords=p,
            coords=ax.transAxes,
            axes=ax
        )
        p.set_path_effects([pe.FillImage(image_bbox)])

# ax.set(xlim=(0, 100), ylim=(0, 100))
box = s.viewbox
ax.set(xlim=(box[0], box[2]), ylim=(box[1], box[3]))

plt.show()
