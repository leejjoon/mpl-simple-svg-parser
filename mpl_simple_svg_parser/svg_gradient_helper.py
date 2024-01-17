import xml.etree.ElementTree as ET
from .svg_mpl_path_iterator import remove_ns


# FIXME: for the pattern, we may create image from the cairosvg result. picosvg
# support fo pattern s incorrect (w/ my modification) or limited.

class GradientHelper:
    def __init__(self, svg):
        self.svg = svg # instance of SVGMplPathIterator
        box = self.svg.viewbox
        self.width, self.height = box[2], box[3]

    def list_gradient(self):
        el = self.svg.svg.find("defs")
        if el is None:
            return []
        else:
            return list(self.svg.svg.find("defs"))

    def get_svg(self, gradient_elem, add_all=False):
        template = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
             height="{height}" width="{width}">
          <defs>
          </defs>
          <rect fill="url(#{gid})" height="100%" width="100%"/>
        </svg>
        """

        box = self.svg.viewbox
        v = dict(width=box[2], height=box[3], gid=gradient_elem.attrib["id"])
        template = remove_ns(template.format(**v).encode("ascii"))
        svg_template = ET.fromstring(template)
        defs = svg_template.find("defs")

        if add_all:
            for el in self.list_gradient():
                defs.append(el)
        else:
            defs.append(gradient_elem)

        k = ET.tostring(svg_template)

        return k

    @classmethod
    def get_gradient_image(cls, svg_string):
        import cairosvg
        png = cairosvg.svg2png(svg_string)

        # from .cairo_numpy_surface import convert_to_numpy
        # arr = convert_to_numpy(k)  / 255.
        # FIXME for some reason, using convert_to_numpy produce incorrect array.

        import cairosvg
        import matplotlib.image as mpimg
        import io

        png = cairosvg.svg2png(k)
        arr = mpimg.imread(io.BytesIO(png))

        return arr

    def get(self, gradient_elem, add_all=False):
        k = self.get_svg(gradient_elem, add_all=add_all)
        arr = self.get_gradient_image(k)

        return arr

    def get_all_svgs(self):
        for gradient_elem in self.list_gradient():
            gid = gradient_elem.attrib.get("id", None)
            if gid is None:
                continue
            if gradient_elem.tag == "pattern":
                # We should add only necessary elements, not all elements.
                k = self.get_svg(gradient_elem, add_all=True)
            else:
                k = self.get_svg(gradient_elem, add_all=False)
            yield gid, k

    def get_all(self):
        gradient_dict = dict()

        for gid, k in self.get_all_svgs():
            arr = self.get_gradient_image(k)
            gradient_dict[gid] = arr

        return gradient_dict
