#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jae-Joon Lee.
# Distributed under the terms of the Modified BSD License.

__all__ = [
    "SVGPathIterator",
    "SVGMplPathIterator",
    "get_paths_extents"
]

import numpy as np
import warnings
import numpy as np
# import io
import cairosvg
from svgpath2mpl import parse_path
import xml.etree.ElementTree as ET
from matplotlib.patches import PathPatch
import matplotlib.colors as mcolors
from matplotlib.collections import PathCollection
from matplotlib.transforms import Affine2D

import re
p_rgb_color = re.compile(r"rgb\((.+)\%,\s*(.+)\%,\s*(.+)\%\)")
p_hex_color = re.compile(r"(#[0-9a-fA-F]+)")

p_namespace = re.compile(r'\s+xmlns="[^"]+"')
p_empty_color = re.compile(r'fill\s*=\s*(\"\"|\'\')')

p_matrix = re.compile(r"matrix\s*\((.+)\)")
p_comma_or_space = re.compile(r"(,|(\s+))")
p_key_value = re.compile(r"([^:\s]+)\s*:\s*(.+)")

def remove_ns(xmlstring):
    xmlstring = p_namespace.sub('', xmlstring, count=1)
    return xmlstring

def fix_empty_color_string(xmlstring):
    """
    cairosvg seems to remove object with 'fill=""'. This replace it with 'fill="#000000"'.
    """
    xmlstring = p_empty_color.sub('fill="#000000"', xmlstring, count=0)
    return xmlstring

def parse_style(style_string):
    style_dict = dict()
    for s in style_string.split(";"):
        if m := p_key_value.match(s.strip()):
            k, v = m.groups()
            style_dict[k] = v

    return style_dict

def convert_svg_color_to_mpl_color(color_string, default_color="none"):
    """
    If possible, convert rgb definition in svg color to 3-element numpy array normalized to 1. Return the original string otherwise.
    """
    if m := p_rgb_color.search(color_string):
        return np.array([float(_)/100. for _ in m.groups()])

    return default_color if color_string == "" else color_string


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


class SVGPathIterator:
    """
    Iterate over path definition of svg file. By default, it uses cairosvg to convert the input svg to more manageable form.
    """
    def __init__(self, s, svg2svg=True):

        if svg2svg:
            xmlstring = fix_empty_color_string(s)
            b_xmlstring = cairosvg.svg2svg(xmlstring, parent_width=800)
            xmlstring = remove_ns(b_xmlstring.decode("ascii"))
        else:
            xmlstring = remove_ns(s)

        self.svg = ET.fromstring(xmlstring)

    def iter_path_attrib(self):
        for c in self.svg.iter():
            if c.tag == "path":
                d = c.attrib["d"]
            else:
                continue

            yield d, c.attrib


class SVGMplPathIterator(SVGPathIterator):

    def get_patch_prop_from_attrib(self, attrib):
        style = parse_style(attrib.get("style", ""))

        fc, ec = get_mpl_colors(attrib, style)

        try:
            mcolors.to_rgb(fc)
        except ValueError:
            warnings.warn(f"Ignoring unsupported facecolor: {fc}")
            return None

        try:
            mcolors.to_rgb(ec)
        except ValueError:
            warnings.warn(f"Ignoring unsupported edgecolor: {ec}")
            return None

        linewidth = float(style.get('stroke-width', 1))

        return dict(fc=fc, ec=ec, lw=linewidth)

    def get_affine_matrix(self, attrib):
        st = attrib.get("transform", "")

        if st.startswith('matrix'):
            m = p_matrix.match(st)
            coords = m.groups()[0]
            if "," in coords:
                cc = coords.split(",")
            else:
                cc = coords.split()
            matrix = np.array([float(_) for _ in cc]).reshape(-1, 2).T
            matrix = np.vstack([matrix, [0, 0, 1]])
        else:
            matrix = np.array([[1, 0, 0],
                               [0, 1, 0],
                               [0, 0, 1]])

        return matrix

    def get_yinvert_transform(self):
        height = (float(self.svg.attrib["viewBox"].split()[-1])
                  if  "viewBox" in self.svg.attrib
                  else 0)

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

    def get_path_collection(self):
        paths = []
        fcl = []
        ecl = []
        lwl = []

        for p, d in self.iter_mpl_path_patch_prop():
            paths.append(p)
            fcl.append(d["fc"])
            ecl.append(d["ec"])
            lwl.append(d["lw"])

        pc = PathCollection(paths, facecolors=fcl, edgecolors=ecl, linewidths=lwl)
        return pc

def get_paths_extents(paths):
    bb = [p.get_extents() for p in paths]
    b0 = bb[0].union(bb)

    return b0


