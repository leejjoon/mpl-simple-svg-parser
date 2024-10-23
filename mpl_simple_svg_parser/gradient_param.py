from typing import NamedTuple, List, Tuple
import numpy as np
from dataclasses import dataclass

class Point(NamedTuple):
    x: float
    y: float


class RGB(NamedTuple):
    r: float
    g: float
    b: float


@dataclass
class GradientParamBase:
    el_id: str
    tag: str
    oca_list: List[Tuple[float, RGB, float]]
    gradientTransform: np.ndarray


@dataclass
class GradientParam(GradientParamBase):
    # el_id: str
    # tag: str
    # oca_list: List[Tuple[float, RGB, float]]
    # gradientTransform: np.ndarray
    pt1: Point
    pt2: Point


@dataclass
class GradientParamRadial(GradientParamBase):
    # el_id: str
    # tag: str
    # pt1: Point
    # pt2: Point
    # oca_list: List[Tuple[float, RGB, float]]
    # gradientTransform: np.ndarray
    c: Point
    fc: Point
    r: float
    fr: float
