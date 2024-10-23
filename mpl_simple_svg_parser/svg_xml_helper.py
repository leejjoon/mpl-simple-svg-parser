import numpy as np
import re
p_rgb_color = re.compile(r"rgb\((.+)\%,\s*(.+)\%,\s*(.+)\%\)")
p_rgb_color_no_percent = re.compile(r"rgb\((.+),\s*(.+),\s*(.+)\)")
p_hex_color = re.compile(r"(#[0-9a-fA-F]+)")

p_namespace = re.compile(rb'xmlns="[^"]+"')
p_namespace_xlink = re.compile(rb'xmlns\:xlink="[^"]+"')
p_xlink_xlink = re.compile(r'xmlns\:xlink="[^"]+"')
p_empty_color = re.compile(rb'fill\s*=\s*(\"\"|\'\')')

p_matrix = re.compile(r"matrix\s*\((.+)\)")
p_comma_or_space = re.compile(r"(,|(\s+))")
p_key_value = re.compile(r"([^:\s]+)\s*:\s*(.+)")

def remove_ns(xmlstring: bytes) -> bytes:
    xmlstring = p_namespace.sub(b'', xmlstring, count=1)
    xmlstring = p_namespace_xlink.sub(b'xmlns:xlink="xlink"', xmlstring, count=1)
    return xmlstring

def fix_empty_color_string(xmlstring: bytes) -> bytes:
    """
    cairosvg seems to remove object with 'fill=""'. This replace it with 'fill="#000000"'.
    """
    xmlstring = p_empty_color.sub(b'fill="#000000"', xmlstring, count=0)
    return xmlstring

def parse_style(style_string):
    style_dict = dict()
    for s in style_string.split(";"):
        if m := p_key_value.match(s.strip()):
            k, v = m.groups()
            style_dict[k] = v

    return style_dict

def convert_svg_affine_to_array(s):
    m = p_matrix.match(s)
    coords = m.groups()[0]
    # cc = p_comma_or_space.split(coords)
    if "," in coords:
        cc = coords.split(",")
    else:
        cc = coords.split()
    matrix = np.array([float(_) for _ in cc]).reshape(-1, 2).T
    matrix = np.vstack([matrix, [0, 0, 1]])

    return matrix


def convert_svg_color_to_rgb_tuple(color_string):
    """
    """
    if m := p_rgb_color.search(color_string):
        return tuple(float(_)/100 for _ in m.groups())
    elif m := p_rgb_color_no_percent.search(color_string):
        return tuple(float(_)/255 for _ in m.groups())
    else:
        raise ValueError(f"unrecognized color value: {color_string}")


def convert_svg_color_to_mpl_color(color_string, default_color="none"):
    """
    If possible, convert rgb definition in svg color to 3-element numpy array normalized to 1. Return the original string otherwise.
    """
    try:
        rgb_tuple = convert_svg_color_to_rgb_tuple(color_string)
        return np.array(rgb_tuple)
    except ValueError:
        return default_color if color_string == "" else color_string


#     if m := p_rgb_color.search(color_string):
#         return np.array([float(_)/100. for _ in m.groups()])
#     if m := p_rgb_color_no_percent.search(color_string):
#         return np.array([float(_)/256. for _ in m.groups()])



# def convert_svg_color_to_rgb(color_string):
#     """
#     If possible, convert rgb definition in svg color to 3-element numpy array normalized to 1. Return the original string otherwise.
#     """
#     if m := p_rgb_color.search(color_string):
#         t = tuple(float(_)/100 for _ in m.groups())
#     elif m := p_rgb_color_no_percent.search(color_string):
#         t = tuple(float(_)/255 for _ in m.groups())
#     else:
#         raise ValueError(f"unrecognized color value: {color_string}")

#     return t
