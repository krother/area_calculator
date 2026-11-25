"""Shape models that can move and draw themselves."""
from typing import Self

import cv2
import numpy as np
from pydantic import BaseModel

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (192, 0, 192)
BLUE = (192, 0, 0)
ORANGE = (0, 128, 255)  # blue-green-red

MAXX = 1200
MAXY = 800

Color = tuple[int, int, int]


class Move(BaseModel):
    xspeed: int = 0
    yspeed: int = 0
    scale_mod: int = 0
    color_mod: tuple[int, int, int] = (0, 0, 0)

    def apply_move(self, shape: "Shape") -> None:
        """Move, rescale and recolor a shape by one step."""
        shape.x += self.xspeed
        shape.y += self.yspeed
        shape.modify_scale(self.scale_mod)
        a, b, c = (
            (x + y) % 256 for x, y in zip(shape.color, self.color_mod)
        )
        shape.color = (a, b, c)


class Shape(BaseModel):
    x: int = 128
    y: int = 128
    color: Color = BLUE
    move: Move = Move()

    def modify_scale(self, mod: int) -> None:
        """Change the size of the shape (does nothing by default)."""

    def draw(self, frame: np.ndarray) -> None:
        """Draw the shape onto the frame."""
        raise NotImplementedError


class Square(Shape):
    size: int

    def draw(self, frame: np.ndarray) -> None:
        """Draw the square onto the frame."""
        frame[self.y:self.y + self.size,
              self.x:self.x + self.size] = self.color

    def modify_scale(self, mod: int) -> None:
        """Grow or shrink the square."""
        self.size += mod


class Circle(Shape):
    radius: int

    def _draw_circle(self, frame: np.ndarray, radius: int, color: Color) -> None:
        """Fill a circle around the shape center."""
        Y, X = np.ogrid[0:MAXY, 0:MAXX]
        square_dist = (X - self.x) ** 2 + (Y - self.y) ** 2
        frame[square_dist < radius ** 2] = color

    def draw(self, frame: np.ndarray) -> None:
        """Draw the circle onto the frame."""
        self._draw_circle(frame, self.radius, self.color)

    def modify_scale(self, mod: int) -> None:
        """Grow or shrink the circle."""
        self.radius += mod


class Donut(Circle):
    inner_radius: int

    def draw(self, frame: np.ndarray) -> None:
        """Draw the donut onto the frame."""
        super().draw(frame)
        self._draw_circle(frame, self.inner_radius, BLACK)  # the hole

    def modify_scale(self, mod: int) -> None:
        """Grow or shrink the donut."""
        super().modify_scale(mod)
        self.inner_radius += mod


class Triangle(Shape):
    edge_length: int
    direction: int  # -1 or 1

    def draw(self, frame: np.ndarray) -> None:
        """Draw an equilateral triangle. Direction is -1/1."""
        height = self.edge_length * np.sqrt(3) / 2
        points = np.array([
            [self.x, self.y - self.direction * 2 * height / 3],
            [self.x - self.edge_length / 2, self.y + self.direction * height / 3],
            [self.x + self.edge_length / 2, self.y + self.direction * height / 3],
        ])
        cv2.fillPoly(frame, [np.round(points).astype(np.int32)], self.color)

    def modify_scale(self, mod: int) -> None:
        """Grow or shrink the triangle."""
        self.edge_length += mod

    @classmethod
    def blue_upsidedown_triangle(cls, x: int, y: int) -> Self:
        """Create a small blue triangle pointing down."""
        return cls(x=x, y=y, edge_length=42, color=BLUE, direction=-1)


# TODO: could implement a Serializer method in Shape that exports a shape object to JSON
SHAPE_CLASSES: dict[str, type[Shape]] = {
    cls.__name__: cls for cls in (Square, Circle, Donut, Triangle)
}

# penguin
