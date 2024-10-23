import io
import numpy as np
import cairocffi as cairo
from cairosvg.surface import Surface, PNGSurface
from cairosvg.parser import Tree
from cairosvg.colors import negate_color
from cairosvg.image import invert_image

class NumpySurface(Surface):
    """A surface that returns numpy array."""
    device_units_per_user_units = 1

    def _create_surface(self, width, height):
        """Create and return ``(cairo_surface, width, height)``."""
        width = int(width)
        height = int(height)

        cairo_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        # cairo_surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)

        return cairo_surface, width, height

    def finish(self):

        w, h = self.width, self.height
        super().finish()
        buf = self.cairo.get_data()
        arr_ = np.ndarray (shape=(h, w, 4), dtype=np.uint8, buffer=buf,
                           order="C",
                           # strides=[self.cairo.get_stride(), 1]
                           )
        arr = np.empty(shape=arr_.shape, dtype=np.uint8, order="C")

        arr[:, :, :-1] = arr_[:, :, -2::-1] # * arr_[:, :, -1:]
        arr[:, :, -1] = arr_[:, :, -1] # * arr_[:, :, -1:]
        # return arr/255.
        return self.divide_alpha(arr/255.)

    def divide_alpha(self, arr):
        """
        Cairo's RGB has values pre-multiplied by alpha. Matplotlib expects straight alpha.
        We divide RGB with alpha.

        (https://en.wikipedia.org/wiki/Alpha_compositing#Straight_versus_premultiplied)

        """
        msk = arr[:, :, -1] ==  0
        alpha = arr[:, :, -1:]

        arr[~msk, :-1] /= alpha[~msk]
        np.clip(arr, 0, 1, out=arr) # for some reason, canvas.get_data
                                    # sometimes have noisy values leading to warning.

        return arr


def convert_to_numpy(bytestring=None, *, file_obj=None, url=None, dpi=96,
                     parent_width=None, parent_height=None, scale=1, unsafe=False,
                     background_color=None, negate_colors=False,
                     invert_images=False, output_width=None,
                     output_height=None, **kwargs):
        """Convert an SVG document to numpy array.

        Specify the input by passing one of these:

        :param bytestring: The SVG source as a byte-string.
        :param file_obj: A file-like object.
        :param url: A filename.

        Give some options:

        :param dpi: The ratio between 1 inch and 1 pixel.
        :param parent_width: The width of the parent container in pixels.
        :param parent_height: The height of the parent container in pixels.
        :param scale: The ouptut scaling factor.
        :param unsafe: A boolean allowing external file access, XML entities
                       and very large files
                       (WARNING: vulnerable to XXE attacks and various DoS).

        Only ``bytestring`` can be passed as a positional argument, other
        parameters are keyword-only.

        """
        if background_color is None:
            # if None is used, it seems that background is set to (0, 0, 0, 1)
            # by default and rendered results has black-ish boundary. Using
            # "background" sets the background to (0, 0, 0, 0) and things are
            # better.
            background_color = None
            # background_color = "background" # setting it to 'background' gets
            # tha rgb correct but alpha gets 1 everywhere.

        tree = Tree(
            bytestring=bytestring, file_obj=file_obj, url=url, unsafe=unsafe,
            **kwargs)
        output = None
        instance = NumpySurface(
            tree, output, dpi, None, parent_width, parent_height, scale,
            output_width, output_height, background_color,
            map_rgba=negate_color if negate_colors else None,
            map_image=invert_image if invert_images else None)
        arr = instance.finish()

        return arr


def svg2numpy(bytestring=None, *, file_obj=None, url=None, dpi=96,
              parent_width=None, parent_height=None, scale=1, unsafe=False,
              background_color=None, negate_colors=False, invert_images=False,
              output_width=None, output_height=None):
    arr = convert_to_numpy(
        bytestring=bytestring, file_obj=file_obj, url=url, dpi=dpi,
        parent_width=parent_width, parent_height=parent_height, scale=scale,
        background_color=background_color, negate_colors=negate_colors,
        invert_images=invert_images, unsafe=unsafe,
        output_width=output_width, output_height=output_height)
    return arr


if __name__ == '__main__':
# if True:
    import io
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg

    # bytestring = open("output.svg", "rb").read()
    # bytestring = b'<svg height="92.995733" width="96.0">\n          <defs>\n          <radialGradient id="radial24" gradientUnits="userSpaceOnUse" cx="-925" cy="-107" fx="-925" fy="-107" r="363" gradientTransform="matrix(0.0228734,0.0253314,-0.0120512,0.0108905,96.628814,75.44808)">\n<stop offset="0" style="stop-color:rgb(31.372549%,57.254902%,100%);stop-opacity:1;" />\n<stop offset="1" style="stop-color:rgb(24.705882%,37.254902%,100%);stop-opacity:1;" />\n</radialGradient>\n</defs>\n          <rect fill="url(#radial24)" height="100%" width="100%" />\n        </svg>'
    # bytestring = b'<svg height="92.995733" width="96.0">\n          <defs>\n          <radialGradient id="radial0" gradientUnits="userSpaceOnUse" cx="-2109.993" cy="780.997" fx="-2109.993" fy="780.997" r="2395.992" gradientTransform="matrix(-0.0267276,0.0298085,0.0298085,0.0267276,-8.248046,75.57064)">\n<stop offset="0" style="stop-color:rgb(100%,95.686275%,47.058824%);stop-opacity:1;" />\n<stop offset="0.475" style="stop-color:rgb(100%,69.019608%,18.039216%);stop-opacity:1;" />\n<stop offset="1" style="stop-color:rgb(96.862745%,3.921569%,55.294118%);stop-opacity:1;" />\n</radialGradient>\n</defs>\n          <rect fill="url(#radial0)" height="100%" width="100%" />\n        </svg>'
    # bytestring = b'<svg height="92.995733" width="96.0">\n          <defs>\n          <radialGradient id="radial1" gradientUnits="userSpaceOnUse" cx="-1400.994" cy="1214.995" fx="-1400.994" fy="1214.995" r="1405.994" gradientTransform="matrix(-0.00612174,0.0306487,0.0392512,0.00784223,-8.248046,75.57064)">\n<stop offset="0.788" style="stop-color:rgb(96.078431%,58.823529%,22.352941%);stop-opacity:0;" />\n<stop offset="0.973" style="stop-color:rgb(100%,49.019608%,80.784314%);stop-opacity:1;" />\n</radialGradient>\n</defs>\n          <rect fill="url(#radial1)" height="100%" width="100%" />\n        </svg>'

    bytestring = b'<svg height="92.995733" width="96.0">\n          <defs>\n          <radialGradient id="radial13" gradientUnits="userSpaceOnUse" cx="-1594" cy="-2272" fx="-1594" fy="-2272" r="773" gradientTransform="matrix(0,0.0105149,0.00491607,0,92.41328,80.33435)">\n<stop offset="0" style="stop-color:rgb(100%,87.843137%,27.058824%);stop-opacity:1;" />\n<stop offset="1" style="stop-color:rgb(100%,87.058824%,26.666667%);stop-opacity:0;" />\n</radialGradient>\n</defs>\n          <rect fill="url(#radial13)" height="100%" width="100%" />\n        </svg>'
    arr1 = convert_to_numpy(bytestring)

    from cairosvg import svg2png
    png = svg2png(bytestring)
    arr2 = mpimg.imread(io.BytesIO(png))

    fig, axs = plt.subplots(5, 2, num=1, clear=True)
    axs[0][0].imshow(arr1[:, :, ], interpolation=None)
    axs[0][1].imshow((arr2)[:, :, ], interpolation=None)
    for i in range(4):
        axs[i+1][0].imshow(arr1[:, :, i], interpolation=None)
        axs[i+1][1].imshow((arr2)[:, :, i], interpolation=None)

    plt.show()
