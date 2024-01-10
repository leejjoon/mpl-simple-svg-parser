"""
A modified version of picosvg.SVG to better ignore exceptions and etc.
"""

import copy
from lxml import etree  # pytype: disable=import-error
from picosvg.svg_transform import Affine2D
from picosvg.svg import SVG as _SVG
from picosvg.svg_meta import (
    svgns
)

from picosvg.svg import (
    _xlink_href_attr_name,
    _try_remove_group,
    _inherit_attrib
)

class SVG(_SVG):

    # We need this to be redefined for "topicosvg" to work.
    def _clone(self) -> "SVG":
        return SVG(svg_root=copy.deepcopy(self.svg_root))

    # a modified version to gave skip_unandled=True for _inherit_attrib
    def _resolve_use(self, scope_el):
        attrib_not_copied = {
            "x",
            "y",
            "width",
            "height",
            "transform",
            _xlink_href_attr_name(),
        }

        # capture elements by id so even if we change it they remain stable
        el_by_id = {el.attrib["id"]: el for el in self.xpath(".//svg:*[@id]")}

        while True:
            swaps = []
            use_els = list(self.xpath(".//svg:use", el=scope_el))
            if not use_els:
                break
            for use_el in use_els:
                ref = use_el.attrib.get(_xlink_href_attr_name(), "")
                if not ref.startswith("#"):
                    raise ValueError(f"Only use #fragment supported, reject {ref}")

                target = el_by_id.get(ref[1:], None)
                if target is None:
                    raise ValueError(f"No element has id '{ref[1:]}'")

                new_el = copy.deepcopy(target)
                # leaving id's on <use> instantiated content is a path to duplicate ids
                for el in new_el.getiterator("*"):
                    if "id" in el.attrib:
                        del el.attrib["id"]

                group = etree.Element(f"{{{svgns()}}}g", nsmap=self.svg_root.nsmap)
                affine = Affine2D.identity().translate(
                    float(use_el.attrib.get("x", 0)), float(use_el.attrib.get("y", 0))
                )

                if "transform" in use_el.attrib:
                    affine = Affine2D.compose_ltr(
                        (
                            affine,
                            Affine2D.fromstring(use_el.attrib["transform"]),
                        )
                    )

                if affine != Affine2D.identity():
                    group.attrib["transform"] = affine.tostring()

                for attr_name in use_el.attrib:
                    if attr_name in attrib_not_copied:
                        continue
                    group.attrib[attr_name] = use_el.attrib[attr_name]

                group.append(new_el)

                if _try_remove_group(group, push_opacity=False):
                    ## START of change for mpl-simple-svg-parser
                    _inherit_attrib(group.attrib, new_el, skip_unhandled=True)
                    ## END
                    swaps.append((use_el, new_el))
                else:
                    swaps.append((use_el, group))

            for old_el, new_el in swaps:
                old_el.getparent().replace(old_el, new_el)

    # a modified version that does not raise exception for any violations.
    def topicosvg(
        self, *, ndigits=3, inplace=False, allow_text=False, drop_unsupported=False
    ):
        if not inplace:
            svg = self._clone()
            svg.topicosvg(
                ndigits=ndigits,
                inplace=True,
                allow_text=allow_text,
                drop_unsupported=drop_unsupported,
            )
            return svg

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

        # Tidy up
        self.evenodd_to_nonzero_winding(inplace=True)
        self.normalize_opacity(inplace=True)
        self.absolute(inplace=True)
        self.round_floats(ndigits, inplace=True)

        # https://github.com/googlefonts/picosvg/issues/269 remove empty subpaths *after* rounding

        self.remove_empty_subpaths(inplace=True)
        self.remove_unpainted_shapes(inplace=True)

        ## START of change for mpl-simple-svg-parser
        # violations = self.checkpicosvg(
        #    allow_text=allow_text, drop_unsupported=drop_unsupported
        # )
        # if violations:
        #     raise ValueError("Unable to convert to picosvg: " + ",".join(violations))
        ## END

        return self
