import numpy as np
import cairocffi as cairo
from cairosvg.surface import Surface
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

        return cairo_surface, width, height

    def finish(self):

        w, h = self.width, self.height
        buf = self.cairo.get_data()
        arr_ = np.ndarray (shape=(h, w, 4), dtype=np.uint8, buffer=buf,
                           order="C",
                           # strides=[self.cairo.get_stride(), 1]
                           )
        arr = np.empty(shape=arr_.shape, dtype=np.uint8, order="C")

        arr[:, :, :-1] = arr_[:, :, -2::-1]
        arr[:, :, -1] = arr_[:, :, -1]
        super().finish()

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
            background_color = "background"

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
    return convert_to_numpy(
        bytestring=bytestring, file_obj=file_obj, url=url, dpi=dpi,
        parent_width=parent_width, parent_height=parent_height, scale=scale,
        background_color=background_color, negate_colors=negate_colors,
        invert_images=invert_images, unsafe=unsafe,
        output_width=output_width, output_height=output_height)


if __name__ == '__main__':
    import io
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg

    bytestring = open("output.svg", "rb").read()
    arr1 = convert_to_numpy(bytestring)  / 255.

    from cairosvg import svg2png
    png = svg2png(bytestring)
    arr2 = mpimg.imread(io.BytesIO(png))

    fig, axs = plt.subplots(1, 2, num=1, clear=True)
    axs[0].imshow(arr1, interpolation=None)
    im = axs[1].imshow(arr2, interpolation=None)

    plt.show()
