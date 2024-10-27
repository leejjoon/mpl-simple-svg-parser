import numpy as np
import xml.etree.ElementTree as ET

from skia_gradient_array import GradientCanvas, Stops

import cairosvg
import matplotlib.image as mpimg
import io
import logging

# FIXME Now that we use skia surface by default, it would be better to
# eliminate cairo_numpy_surface and simplify the code.

from .cairo_numpy_surface import convert_to_numpy

from .svg_xml_helper import (
    remove_ns,
    convert_svg_color_to_rgb_tuple,
    parse_style,
    convert_svg_affine_to_array,
)

# FIXME: for the pattern, we may create image from the cairosvg result. picosvg
# support fo pattern s incorrect (w/ my modification) or limited.

from .gradient_param import Point, RGB, GradientParam, GradientParamRadial

# A base class. It will create an svg element based on the etmplate and use cairosvg to render.

class GradientHelperBase:
    def __init__(self, svg, use_png=False):
        self.svg = svg # instance of SVGMplPathIterator
        box = self.svg.viewbox
        self.width, self.height = box[2], box[3]
        self._gradient_cache = dict()
        self._use_png = use_png

    def list_gradient(self):
        el = self.svg.svg.find("defs")
        if el is None:
            return []
        else:
            return list(self.svg.svg.find("defs"))

    _template = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
             height="{height}" width="{width}">
          <defs>
          </defs>
          <rect fill="url(#{gid})" height="100%" width="100%"/>
        </svg>
        """

    def get_svg(self, gradient_elem, add_all=None):
        """
        add_all: True | False | None. None means True only if its tag is "pattern".
        """
        if add_all is None:
            if gradient_elem.tag == "pattern":
                add_all = True
            else:
                add_all = False

        box = self.svg.viewbox
        v = dict(width=box[2], height=box[3], gid=gradient_elem.attrib["id"])
        template = remove_ns(self._template.format(**v).encode("ascii"))
        svg_template = ET.fromstring(template)
        defs = svg_template.find("defs")

        if add_all:
            for el in self.list_gradient():
                defs.append(el)
        else:
            defs.append(gradient_elem)

        k = ET.tostring(svg_template)

        return k

    def get_gradient_image_cairo(self, svg_string):

        if self._use_png:
            png = cairosvg.svg2png(svg_string)
            arr = mpimg.imread(io.BytesIO(png))
        else:
            arr = convert_to_numpy(svg_string)

        return arr[:, :, :]

    def get(self, gradient_elem, add_all=None):
        k = self.get_svg(gradient_elem, add_all=add_all)
        arr = self.get_gradient_image_cairo(k)

        return arr

    def iter_gradient_elem(self):
        for gradient_elem in self.list_gradient():
            gid = gradient_elem.attrib.get("id", None)
            if gid is None:
                continue
            yield gid, gradient_elem

    # def iter_all_svgs(self):
    #     for gid, gradient_elem in self.iter_gradient_elem():
    #         k = self.get_svg(gradient_elem)
    #         yield gid, k

    def get_all(self, use_cache=True):
        if use_cache:
            gradient_dict = self._gradient_cache
        else:
            gradient_dict = dict()

        for gid, gradient_elem in self.iter_gradient_elem():
            if gid not in gradient_dict:
                arr = self.get_gradient_from_elem(gid, gradient_elem)
                gradient_dict[gid] = arr

        # gradient_dict = self._get_all_gradients()

        return gradient_dict

    def get_gradient_from_elem(self, el_id, el):
        k = self.get_svg(el)
        arr = self.get_gradient_image_cairo(k)

        return arr

    def get_gradient_param(self, el_id, el):
        grad_attrib = el.attrib
        grad_stops = list(el.iterfind("stop"))

        try:
            gradientTransform_ = (convert_svg_affine_to_array(grad_attrib["gradientTransform"])
                                  if "gradientTransform" in grad_attrib else None)
        except:
            # FIXME what is the correct behavior?
            return

        oca_list = [] # offset, color, alpha
        for a in grad_stops:
            o = float(a.attrib["offset"])
            if "style" in a.attrib:
                style = parse_style(a.attrib["style"])
            else:
                style = a.attrib
            c = convert_svg_color_to_rgb_tuple(style["stop-color"])
            a = float(style.get("stop-opacity", 1))

            oca_list.append((o, c, a))

        if el.tag == "radialGradient":
            c = Point(float(grad_attrib["cx"]), float(grad_attrib["cy"]))
            fc = Point(float(grad_attrib.get("fx", c.x)),
                       float(grad_attrib.get("fy", c.y)))

            r = float(grad_attrib["r"])
            fr = float(grad_attrib.get("fr", 0))

            gp = GradientParamRadial(el_id, el.tag, oca_list, gradientTransform_,
                                     c, fc, r, fr)

        elif el.tag == "linearGradient":
            pt1 = Point(float(grad_attrib["x1"]), float(grad_attrib["y1"]))
            pt2 = Point(float(grad_attrib["x2"]), float(grad_attrib["y2"]))

            gp = GradientParam(el_id, el.tag, oca_list, gradientTransform_, pt1, pt2)

        else:
            logging.warn(f"No support for {el.tag}")
            return None
            # raise ValueError("No support for ", el.tag)

        return gp

    def iter_gradient_param(self):

        for el_id , el in self.iter_gradient_elem():
            yield self.get_gradient_param(el_id, el)



# Skia base gradient gneerator
class GradientHelper(GradientHelperBase):
    def __init__(self, svg):
        GradientHelperBase.__init__(self, svg, use_png=True)

    def get_gradient_from_elem(self, el_id, el):

        param = self.get_gradient_param(el_id, el)
        if param is None:
            return None

        w, h = int(self.width), int(self.height)

        gradientTransform = (None if param.gradientTransform is None
                             else list(np.ravel(param.gradientTransform[:-1].T)))

        stops = Stops(param.oca_list)
        canvas = GradientCanvas(w, h)
        if param.tag == "linearGradient":
            arr = canvas.makeLinear(param.pt1, param.pt2, stops, gradientTransform).get_array()
        elif param.tag == "radialGradient":
            arr = canvas.makeRadial(param.fc, param.fr, param.c, param.r,
                                    stops, gradientTransform).get_array()
        else:
            logging.debug("Skia backend does not support {param.tag} tag. Falling back to the default backend.")
            arr = GradientHelperBase.get_gradient_from_elem(self, el_id, el)

        return arr
