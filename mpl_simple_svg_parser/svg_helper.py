import re

import numpy as np
from matplotlib.patches import PathPatch
from matplotlib.offsetbox import DrawingArea # , AnnotationBbox
# from mpl_simple_svg_parser import SVGMplPathIterator

from .svg_gradient_hlper import GradientHelper

import mpl_visual_context.patheffects as pe
from mpl_visual_context.image_box import ImageBox

p_url = re.compile(r"url\(#(.+)\)")


def get_svg_drawing_area(ax, svg_mpl_path_iterator, wmax=np.inf, hmax=np.inf):

    gh = GradientHelper(svg_mpl_path_iterator)
    gradient_dict = gh.get_all()

    x1, y1, w, h = svg_mpl_path_iterator.viewbox

    if wmax == np.inf and hmax == np.inf:
        scale = 1
    else:
        scale = min([wmax / w, hmax / w])

    da = DrawingArea(scale*w, scale*h)

    for p1, d in svg_mpl_path_iterator.iter_mpl_path_patch_prop():
        if scale != 1:
            p1 = type(p1)(vertices=p1.vertices * scale, codes=p1.codes)
        p = PathPatch(p1, ec=d["ec"], fc=d["fc"], alpha=d["alpha"])
        da.add_artist(p)
        # print(d)

        if (fc_orig := d.get("fc_orig")) and (m := p_url.match(fc_orig)):
            gradient_name = m.group(1)
            arr = gradient_dict.get(gradient_name, None)
            if arr is None: break
            image_bbox = ImageBox(
                arr[::-1],
                extent=[0, 0, scale*w, scale*h],
                coords=da.get_transform(),
                axes=ax
            )
            p.set_path_effects([pe.FillImage(image_bbox)])

    return da


def get_svg_drawing_area_simple(svg_mpl_path_iterator, wmax=np.inf, hmax=np.inf,
                                ec="0.5", fc="none"):

    _, _, w, h = svg_mpl_path_iterator.viewbox

    if wmax == np.inf and hmax == np.inf:
        scale = 1
    else:
        scale = min([wmax / w, hmax / w])

    da = DrawingArea(scale*w, scale*h)

    for p1, _ in svg_mpl_path_iterator.iter_mpl_path_patch_prop():
        if scale != 1:
            p1 = type(p1)(vertices=p1.vertices * scale, codes=p1.codes)
        p = PathPatch(p1, ec=ec, fc=fc)
        da.add_artist(p)

    return da