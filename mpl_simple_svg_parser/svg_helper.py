import re

import numpy as np
from matplotlib.axes import Axes
from matplotlib.patches import PathPatch
from matplotlib.offsetbox import DrawingArea # , AnnotationBbox
# from mpl_simple_svg_parser import SVGMplPathIterator
from matplotlib.transforms import IdentityTransform
from matplotlib.path import Path

import mpl_visual_context.patheffects as pe
from mpl_visual_context.image_box import ImageBox

from .svg_gradient_hlper import GradientHelper

p_url = re.compile(r"url\(#(.+)\)")


def _draw_svg(ax, drawing_area, transform, svg_mpl_path_iterator, scale=1, xy=(0, 0),
              do_gradient=True, use_path_extent=False):

    if do_gradient:
        gh = GradientHelper(svg_mpl_path_iterator)
        gradient_dict = gh.get_all()
    else:
        gradient_dict = {}

    x1, y1, w, h = svg_mpl_path_iterator.viewbox

    if scale != 1 or xy != (0, 0):
        x, y = xy
        extent =[x, y, x + scale*w, y + scale*h]
    else:
        extent =[0, 0, w, h]

    # da, trans = drawing_area, transform
    if isinstance(drawing_area, Axes):
        add_artist = getattr(drawing_area, "add_patch")
    else:
        add_artist = getattr(drawing_area, "add_artist")

    paths, patches = [], []
    if not use_path_extent:  # We initialize the patch temporarily using
                             # IdentityTransform, and update the transform
                             # later with a real one. This was intended not to update
                             # ax.dataLim. Not sure if this is a correct way.
        trans = IdentityTransform()
    else:
        trans = transform

    for p1, d in svg_mpl_path_iterator.iter_mpl_path_patch_prop():
        if scale != 1 or xy is not None:
            p1 = type(p1)(vertices=p1.vertices * scale + xy, codes=p1.codes)
        p = PathPatch(p1, ec=d["ec"], fc=d["fc"], alpha=d["alpha"], transform=trans)
        add_artist(p)

        if (fc_orig := d.get("fc_orig")) and (m := p_url.match(fc_orig)):
            gradient_name = m.group(1)
            arr = gradient_dict.get(gradient_name, None)
            if arr is None:
                p.set_hatch("XX")
            else:
                image_bbox = ImageBox(
                    arr[::-1],
                    extent=extent,
                    coords=transform,
                    axes=ax
                )
                p.set_path_effects([pe.FillImage(image_bbox)])

        paths.append(p1)
        patches.append(p)

    if not use_path_extent:
        for p in patches:
            p.set_transform(transform)

    return paths, patches


def draw_svg(ax, svg_mpl_path_iterator, transform=None, xy=(0, 0), scale=1,
             datalim_mode="viewbox"):
    """

    datalim_mode: 'viewbox' | 'path' | None
    """

    use_path_extent = True if datalim_mode == "path" else False

    if transform is None:
        transform = ax.transData

    paths, patches = _draw_svg(ax, ax, transform, svg_mpl_path_iterator, scale=scale, xy=xy,
                               use_path_extent=use_path_extent)

    if datalim_mode == "viewbox" and transform == ax.transData:
        x1, y1, w, h = svg_mpl_path_iterator.viewbox

        if scale != 1 or xy != (0, 0):
            x1, y1 = xy
            x2, y2 = x1 + scale*w, y1 + scale*h
        else:
            x1, y1 = 0, 0
            x2, y2 = w, h

        path = Path([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
        ax.dataLim.update_from_path(path, ignore=False)

    if datalim_mode in ["viewbox", "path"]:
        ax.autoscale_view()

    return paths, patches


def get_svg_drawing_area(ax, svg_mpl_path_iterator, wmax=np.inf, hmax=np.inf):

    x1, y1, w, h = svg_mpl_path_iterator.viewbox

    if wmax == np.inf and hmax == np.inf:
        scale = 1
    else:
        scale = min([wmax / w, hmax / w])

    da = DrawingArea(scale*w, scale*h)

    _draw_svg(ax, da, da.get_transform(), svg_mpl_path_iterator, scale=scale)

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
