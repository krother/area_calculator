"""
core business logic: area calculation

should depend on as few other modules as possible.
"""
from typing import Literal, Callable


class MathFunctions:
    """define an interface that the core logic needs"""
    # TODO: could go to a separate module: adapters.py or interfaces.py or schema.py

    def lookup_pi(self) -> float:
        pass

    def sqrt(self, x: float) -> float:
        pass


def calc_square(size: int, math_funcs: MathFunctions):
    return size ** 2

def calc_circle(size: int, math_funcs: MathFunctions):
    pi = math_funcs.lookup_pi()  # assume this is external info
    return pi * size ** 2

def calc_triangle(size: int, math_funcs: MathFunctions):
    return size ** 2 * math_funcs.sqrt(3) / 4

def calc_hexagon(size: int, math_funcs: MathFunctions):
    return 6 * calc_triangle(size, math_funcs)


Shape = Literal["triangle", "square", "hexagon", "circle"]

# dispatch dictionary
equations: dict[Shape, Callable[[int, MathFunctions], float]] = {
    "triangle": calc_triangle,
    "square": calc_square,
    "hexagon": calc_hexagon,
    "circle": calc_circle,
}


def calculate_shape_area(name: Shape, size: int, math_funcs: MathFunctions) -> float:
    assert name in equations, "no such shape info"
    func = equations[name]
    area = func(size, math_funcs)
    return area

# TODO: write a test for this module
