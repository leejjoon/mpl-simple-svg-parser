#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jae-Joon Lee.
# Distributed under the terms of the Modified BSD License.

# FIXME:
# 1. we are not parseing things like joinstyle or cap style.
# 2. clippath is parsed from defs but ignored for the rest of the code.
# 3. only symbols are parsed from definitions.

# cairosvg convert g with opacity to a mask. picosvg drops mask unfortunately.
# We may implement mask feature in the future.

__all__ = [
    "SVGPathIterator",
    "SVGMplPathIterator",
    "get_paths_extents"
]

# pico
# * clip-path works better
# * evenodd works.
# * better stroke (stroke is converted to fill)

# issue : 
# + cairosvg convert ellipse to path but does not close it. When picosvg convert the stroke to fill, this may introduce incorrect fill combined with clippath.

import numpy as np
import warnings
import numpy as np
import cairosvg
from svgpath2mpl import parse_path
import xml.etree.ElementTree as ET
from matplotlib.patches import PathPatch
import matplotlib.colors as mcolors
from matplotlib.collections import PathCollection
from matplotlib.transforms import Affine2D

from .svg_xml_helper import (convert_svg_color_to_mpl_color,
                             fix_empty_color_string,
                             parse_style,
                             convert_svg_affine_to_array,
                             remove_ns)
from .svg_gradient_helper import GradientHelper

def get_mpl_colors(attrib, style, fc_default="k", ec_default="none"):
    """
    Try to get mpl color from svg attribute and the style dict.
    """
    fc, ec = "", ""

    for d in [style, attrib]:
        if "fill" in d:
            fc = d["fill"]

    for d in [style, attrib]:
        if "stroke" in d:
            ec = d["stroke"]

    fc = convert_svg_color_to_mpl_color(fc, fc_default)
    ec = convert_svg_color_to_mpl_color(ec, ec_default)

    return fc, ec

def get_alpha(attrib, style):
    """
    Try to get alpha
    """
    alpha = 1
    for d in [style, attrib]:
        if "opacity" in d:
            alpha = float(d["opacity"])
        if "fill-opacity" in d:
            alpha *= float(d["fill-opacity"])

    return alpha


class SVGPathIterator:
    """
    Iterate over path definition of svg file. By default, it uses cairosvg to convert the input svg to more manageable form.
    """
    def __init__(self, s: bytes, svg2svg=True, pico=False,
                 pico_clip_viewbox=True,
                 failover_width=1024, failover_height=1024):

        if svg2svg:
            xmlstring = fix_empty_color_string(s)
            try:
                b_xmlstring = cairosvg.svg2svg(xmlstring)
            except ValueError:
                b_xmlstring = cairosvg.svg2svg(xmlstring,
                                               parent_width=failover_width,
                                               parent_height=failover_height)

        else:
            b_xmlstring = s

        if pico:
            from . import picosvg_helper

            svg = picosvg_helper.SVG.fromstring(b_xmlstring)
            svg = svg.topicosvg(
                allow_text=True, drop_unsupported=False
            )
            if pico_clip_viewbox:
                svg.clip_to_viewbox(inplace=True)
            b_xmlstring = svg.tostring(pretty_print=True).encode("ascii")
            # xmlstring = remove_ns(xmlstring)
            # xmlstring

        self.xmlstring = remove_ns(b_xmlstring)

        self.svg = ET.fromstring(self.xmlstring)

        self.defs = self.parse_defs()

        self.viewbox = self.parse_viewbox()
        self._gradient_helper = None

    def parse_viewbox(self):
        if "viewBox" in self.svg.attrib:
            viewbox = [float(_) for _ in self.svg.attrib["viewBox"].split()]
        elif "width" in self.svg.attrib and "height" in self.svg.attrib:
            viewbox = [0, 0,
                       float(self.svg.attrib["width"]),
                       float(self.svg.attrib["height"])]
        else:
            viewbox = None
        return viewbox

    def _parse_defs(self, parent, defs):
        for c in parent:
            if c.tag == "symbol":
                symbol_id = c.attrib["id"]
                defs[symbol_id] = c
                # defs[symbol_id] = [(c1.attrib["d"], c1.attrib)
                #                    for c1 in c.findall("path")]
            elif c.tag == "clipPath":
                _id = c.attrib["id"]
                defs[_id] = c
            elif c.tag == "g" and "id" in c.attrib:
                _id = c.attrib["id"]
                defs[_id] = c
            elif c.tag == "g":
                self._parse_defs(c, defs)

    def parse_defs(self):
        defs = dict()
        p = self.svg.find("defs")
        if p is None: return defs

        self._parse_defs(p, defs)

        return defs

    def _iter_path_attrib(self, parent, attrib=None):
        if parent is None:
            return

        if attrib is None:
            attrib = {}

        for c in parent:
            if c.tag == "path":
                if "d" in c.attrib:
                    d = c.attrib["d"]
                    yield d, attrib | c.attrib
            elif c.tag == "symbol":
                c1 = c.find("path")
                d = c1.attrib["d"]
                yield d, attrib | c.attrib
            elif c.tag == "use":
                href = c.attrib["{xlink}href"]
                # FIXME: modifying parent's attrib can be potentially dangerous.
                if "transform" in c.attrib:
                    pass
                    # parent.attrib["transform"] = c.attrib["transform"]
                else:
                    x = c.attrib.get("x", 0)
                    y = c.attrib.get("y", 0)

                    parent.attrib["xy"] = float(x), float(y)

                for d, a in self._iter_path_attrib(self.defs.get(href[1:])):
                    yield d, attrib | parent.attrib
                    # print(c1)

            elif c.tag == "g":
                yield from self._iter_path_attrib(c, c.attrib)
            else:
                continue

    def iter_path_attrib(self):

        yield from self._iter_path_attrib(self.svg)


class SVGMplPathIterator(SVGPathIterator):

    def get_patch_prop_from_attrib(self, attrib):
        style = parse_style(attrib.get("style", ""))

        fc, ec = get_mpl_colors(attrib, style)
        fc_orig = None

        # for now we only get the fill-opacity
        alpha = get_alpha(style, attrib)

        try:
            mcolors.to_rgb(ec)
        except ValueError:
            warnings.warn(f"Ignoring unsupported edgecolor: {ec}")
            ec = "0.5"

        try:
            mcolors.to_rgb(fc)
        except ValueError:
            # warnings.warn(f"Ignoring unsupported facecolor: {fc}")
            fc_orig = fc
            fc = "none"

        linewidth = float(style.get('stroke-width', 1))

        return dict(fc=fc, ec=ec, lw=linewidth, alpha=alpha, fc_orig=fc_orig)

    def get_affine_matrix(self, attrib):
        # Not sure if this is rigorous treatment. xy attribute is inserted when
        # symbole is used.
        if "xy" in attrib:
            x, y = attrib["xy"]
            matrix = np.array([[1, 0, x],
                               [0, 1, y],
                               [0, 0, 1]])
            return matrix

        st = attrib.get("transform", "")

        if st.startswith('matrix'):
            matrix = convert_svg_affine_to_array(st)
        else:
            matrix = np.array([[1, 0, 0],
                               [0, 1, 0],
                               [0, 0, 1]])

        return matrix

    def get_yinvert_transform(self):
        height = 0 if self.viewbox is None else self.viewbox[-1]

        tr = Affine2D().scale(1, -1).translate(0, height)

        return tr

    def iter_mpl_path_patch_prop(self, invert_y=True):
        if invert_y:
            tr_yinvert = self.get_yinvert_transform()
        else:
            tr_yinvert = Affine2D()

        for d, attrib in self.iter_path_attrib():
            patch_prop = self.get_patch_prop_from_attrib(attrib)
            if patch_prop is None:
                continue

            p = parse_path(d)
            matrix = self.get_affine_matrix(attrib)
            p = (Affine2D(matrix) + tr_yinvert).transform_path(p)

            yield p, patch_prop

    def get_path_collection(self, use_alpha=False):
        paths = []
        fcl = []
        ecl = []
        lwl = []
        alphal = []

        for p, d in self.iter_mpl_path_patch_prop():
            paths.append(p)
            fcl.append(d["fc"])
            ecl.append(d["ec"])
            lwl.append(d["lw"])
            alphal.append(d["alpha"])

        # FIXME: when alpha is used for the facecolor and the ec is "none", it
        # fails wth some examples (Steps.svg, alphachannel.svg). So, alpha is
        # disabled for now.
        if use_alpha:
            pc = PathCollection(paths, facecolors=fcl, edgecolors=ecl, linewidths=lwl,
                                alpha=alphal)
        else:
            pc = PathCollection(paths, facecolors=fcl, edgecolors=ecl, linewidths=lwl)

        return pc

    def get_gradient_helper(self):
        if self._gradient_helper is None:
            self._gradient_helper = GradientHelper(self)

        return self._gradient_helper


    def draw(self, ax, transform=None, xy=(0, 0), scale=1,
             datalim_mode="viewbox",
             do_gradient=True):
        """
        datalim_mode: 'viewbox' | 'path'
        """

        from .svg_helper import draw_svg
        paths, patches = draw_svg(ax, self, transform=transform, xy=xy, scale=scale,
                                  datalim_mode=datalim_mode,
                                  do_gradient=do_gradient)

        # if autoscale_view:
        #     ax.autoscale_view()

        # for p in patches:
        #     ax._update_patch_limits(p)

        # path = Path(xy)
        # self.update_from_path(path, ignore=ignore,
        #                       updatex=updatex, updatey=updatey)

    def get_drawing_area(self, ax, wmax=np.inf, hmax=np.inf,
                         do_gradient=True):
        from .svg_helper import get_svg_drawing_area
        da = get_svg_drawing_area(ax, self, wmax=wmax, hmax=hmax,
                                  do_gradient=do_gradient)

        return da


def get_paths_extents(paths):
    bb = [p.get_extents() for p in paths]
    if len(bb) == 0:
        return None

    b0 = bb[0].union(bb)

    return b0
