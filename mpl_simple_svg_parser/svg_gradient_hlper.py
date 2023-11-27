import xml.etree.ElementTree as ET
from mpl_simple_svg_parser.svg_mpl_path_iterator import remove_ns, SVGMplPathIterator

class GradientHelper:
    def __init__(self, svg):
        self.svg = svg # instance of SVGMplPathIterator
        box = self.svg.viewbox
        self.width, self.height = box[2], box[3]

    def list_gradient(self):
        return list(self.svg.svg.find("defs"))

    def get(self, gradient_elem):
        template = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
             height="{height}" width="{width}">
          <defs>
          </defs>
          <rect fill="url(#{gid})" height="100%" width="100%"/>
        </svg>
        """

        box = self.svg.viewbox
        v = dict(width=box[2], height=box[3], gid=gradient_elem.attrib["id"])
        template = remove_ns(template.format(**v))
        svg_template = ET.fromstring(template)
        defs = svg_template.find("defs")

        defs.append(gradient_elem)

        k = ET.tostring(svg_template)
        import cairosvg
        png = cairosvg.svg2png(k)

        import matplotlib.image as mpimg
        import io
        arr = mpimg.imread(io.BytesIO(png))

        return arr

    def get_all(self):
        gradient_dict = dict()

        for gradient_elem in self.list_gradient():
            gid = gradient_elem.attrib["id"]
            arr = self.get(gradient_elem)
            gradient_dict[gid] = arr

        return gradient_dict

