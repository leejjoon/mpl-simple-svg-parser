from matplotlib.patches import PathPatch
from mpl_simple_svg_parser.svg_mpl_path_iterator import SVGMplPathIterator
from mpl_simple_svg_parser.svg_gradient_hlper import GradientHelper
from mpl_simple_svg_parser.svg_helper import get_svg_drawing_area

fn = "w3_svg_samples/rg1024_metal_effect.svg"
# fn = "w3_svg_samples/pservers-grad-03-b.svg"
# fn = "w3_svg_samples/juanmontoya_lingerie.svg"
# fn = "w3_svg_samples/python.svg"
# fn = "sphere.svg"
# fn = "svg_pattern.svg"

b_xmlstring = open(fn, "rb").read()
# b_xmlstring = xmlstring.encode("ascii")
s = SVGMplPathIterator(b_xmlstring, pico=True)
u = s.xmlstring
# open("t.svg", "w").write(u)

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
        arr = gradient_dict.get(gradient_name, None)
        if arr is None: break
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
