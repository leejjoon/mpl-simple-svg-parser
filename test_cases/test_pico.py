import cairosvg
import picosvg

"""
tommek_Car # "fill: url(#linearGradient4116) rgb(0, 0, 0)". cairosvg okay.
photos # "0%" in rect. cairosvg handles it and convert it. svg width and height need to be specified though.
circles1 # "cm" unit. cairosvg handles it.
juanmontoya_lingerie # "pt" in unit. cairosvg handles it.
masking-path-04-b # bad tag 'text'. Not clear why. Cairosvg is okay.
rg1024_metal_effect  # error with pattern element
rg1024_Presentation_with_girl # "1 pt"
fsm # ValueError: S has sets of 4 args, 5 invalid. maybe ill-formated? cairosvg handles it.
compuserver_msn_Ford_Focus # id4 unknown attr. cairosvg okay
tommek_Car # Unrecognized url "url(#linearGradient4116) rgb(0, 0, 0)". cairosvg okay
"""

# pick is okay but still error
"""
gaussian1 # pico itself works okay w/o error. not sure why no output.
bozo # pico is okay but still error
"""
# fixed
"""
json # 00
jsonatom #00
duck # 00
ny1 # fixed already. do not remember the problem though.
"""
# no error, incorrect result
"""
dukechain # no eorror, but most shapes are gone.
ubuntu # no error, but result is wrong
lineargradient4
Steps
mememe : colors are wrong
"""

# Incorrect text placement
"""
snake
"""

# FIXME 1 duck.svg, jsonatom : have "00" or "01" which is parsed as two integers by pico. 
"""
juanmontoya_lingerie
rg1024_metal_effect
svg2009
ubuntu
gallardo
pencil
jsonatom # incorrect rendering
rg1024_green_grapes
scimitar
accesible # check rendering
tommek_Car
mememe

"""

"""
pencil : px issue.
"""

input_file = "w3_svg_samples/jsonatom.svg"
input_file = "jjj.svg"
input_file = "tt2.svg"

failover_width = 1024
failover_height = 1024

b_xmlstring = open(input_file, "rb").read()
# try:
#     b_xmlstring = cairosvg.svg2svg(b_xmlstring)
# except ValueError:
#     b_xmlstring = cairosvg.svg2svg(b_xmlstring,
#                                    parent_width=failover_width,
#                                    parent_height=failover_height)

# svg = SVG.parse(input_file)

from mpl_simple_svg_parser import picosvg
svg = picosvg.SVG.fromstring(b_xmlstring.decode("ascii"))

# svg = svg.topicosvg(
#     allow_text=True, drop_unsupported=False
# )

if True:
    ndigits=3
    inplace=False
    allow_text=True
    drop_unsupported=False

    self = svg
    self._update_etree()

    # Discard useless content
    self.remove_nonsvg_content(inplace=True)
    self.remove_processing_instructions(inplace=True)
    self.remove_anonymous_symbols(inplace=True)
    self.remove_title_meta_desc(inplace=True)

    # Simplify things that simplify in isolation
    self.apply_style_attributes(inplace=True)
    self.resolve_nested_svgs(inplace=True)
    self.shapes_to_paths(inplace=True)
    self.expand_shorthand(inplace=True)
    self.resolve_use(inplace=True)

    # Simplify things that do not simplify in isolation
    self.simplify(inplace=True)
    print(self.svg_root[0], list(self.svg_root[0]))

    # Tidy up
    self.evenodd_to_nonzero_winding(inplace=True)
    self.normalize_opacity(inplace=True)
    self.absolute(inplace=True)
    self.round_floats(ndigits, inplace=True)

    # https://github.com/googlefonts/picosvg/issues/269 remove empty subpaths *after* rounding
    self.remove_empty_subpaths(inplace=True)
    self.remove_unpainted_shapes(inplace=True)

    violations = self.checkpicosvg(
        allow_text=allow_text, drop_unsupported=drop_unsupported
    )

 # svg.clip_to_viewbox(inplace=True)
output = svg.tostring(pretty_print=True)

# open("tt.svg", "w").write(output)

if True:
    from mpl_simple_svg_parser import SVGMplPathIterator, get_paths_extents
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 1, figsize=(5, 5), num=1, clear=True)

    svg_mpl_path_iterator = SVGMplPathIterator(output.encode("ascii"), svg2svg=True)
    ax.set_aspect(True)
    # we first set the viewport
    if svg_mpl_path_iterator.viewbox is not None:
        x1, y1, x2, y2 = svg_mpl_path_iterator.viewbox
        ax.set(xlim=(x1, x2), ylim=(y1, y2))

    pc = svg_mpl_path_iterator.get_path_collection()
    ax.add_collection(pc)

    plt.show()

"""
jsonatom
"""
