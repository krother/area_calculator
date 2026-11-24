"""
uv add opencv-python
"""
import random
from typing import Any

import cv2
import numpy as np
from pydantic import BaseModel, field_validator


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
PURPLE = (192, 0, 192)
BLUE = (192, 0, 0)
ORANGE = (0, 128, 255)  # blue-green-red

MAXX = 1200
MAXY = 800

# Why are we using classes?
# - make the code easier to read
# - make the code easier to modify
# - separate stuff that changes from stuff that does not change
#   (or changes for different reasons)

Color = tuple[int, int, int]


class Move(BaseModel):
    xspeed: int = 0
    yspeed: int = 0
    scale_mod: int = 0
    color_mod: tuple[int, int, int] = (0, 0, 0)

    def apply_move(self, shape):
        shape.x += self.xspeed
        shape.y += self.yspeed

        shape.modify_scale(self.scale_mod)

        new_color = tuple((a+b) % 256 for a, b in zip(shape.color, self.color_mod))
        shape.color = new_color


class Shape(BaseModel):
    # attributes
    x: int = 128
    y: int = 128
    color: Color = BLUE
    move: Move = Move()  # object composition

    def modify_scale(self, mod):
        pass

    # would also work with dataclass (standard module)
    # TODO: forbid extra fields with pydantic config option
    # good idea if data does not change: size:int = Field(default=32, gt=0, le=min(MAXX, MAXY))




class Square(Shape):
    size: int

    def draw(self, frame):
        """
        method: a function inside a class
        self: a reference to the object we are currently working on
        """
        frame[self.y:self.y+self.size,
              self.x:self.x+self.size] = self.color

    def modify_scale(self, mod):
        self.size += mod


class Circle(Shape):
    radius: int

    def _draw_circle(self, radius, color):
        Y, X = np.ogrid[0:MAXY, 0:MAXX]
        square_dist = (X - self.x) ** 2 + (Y - self.y) ** 2
        mask = square_dist < radius ** 2
        frame[mask] = color

    def draw(self, frame):
        self._draw_circle(self.radius, self.color)

    def modify_scale(self, mod):
        self.radius += mod


class Donut(Circle):
    """
    inheritance: Donut is a special kind of circle
    it does everything Circle does and more (Liskovs Substitution Principle)
    Circle is the parent class of Donut
    Donut is the child class of Circle
    """
    inner_radius: int
 
    def draw(self, frame):
        super().draw(frame)  # calls Circle.draw()
        self._draw_circle(self.inner_radius, BLACK)  # draw the hole

    def modify_scale(self, mod):
        super().modify_scale(mod)
        self.inner_radius += mod



class Triangle(Shape):
    edge_length: int
    direction: int  # -1 or 1  TODO use Literal

    def draw(self, frame):
        """Draw an upright equilateral triangle. Direction is -1/1."""
        height = self.edge_length * np.sqrt(3) / 2
        points = np.array([
            [self.x, self.y - self.direction * 2 * height / 3],
            [self.x - self.edge_length / 2, self.y + self.direction * height / 3],
            [self.x + self.edge_length / 2, self.y + self.direction * height / 3],
        ])
        cv2.fillPoly(frame, [np.round(points).astype(np.int32)], self.color)

    def modify_scale(self, mod):
        self.edge_length += mod

    @staticmethod
    def blue_upsidedown_triangle(x, y) -> Triangle:
        """
        a special creator method
        @staticmethod : a method without self
        """
        return Triangle(x=x, y=y, edge_length=42, color=BLUE, direction=-1)



# class: abstraction, instance: concrete object
# table: abstraction, row: concrete data

shapes = [
    Donut(x=500, y=500, radius=100, inner_radius=50, color=ORANGE, move=Move(scale_mod=1)),
    Square(size=32, color=GREEN, move=Move(xspeed=1, scale_mod=2)),
    Square(x=900, y=400, size=32),
    Circle(x=200, y=200, radius=64, color=PURPLE, move=Move(yspeed=1)),
    Triangle(x=800, y=500, edge_length=50, color=BLUE, direction=1, move=Move(xspeed=-1, yspeed=-1, color_mod=(0, 0, 1))),
    Triangle.blue_upsidedown_triangle(50, 50)
]
for _ in range(100):
    shapes.append(Square(x=600, y=400, size=random.randint(5,20), 
            color=(random.randint(50,255), random.randint(50,255), random.randint(50,255)),
            move=Move(xspeed=random.randint(-5, 5), yspeed=random.randint(-5, 5))
    ))
               


background = np.zeros((MAXY, MAXX, 3), np.uint8)

while True:
    frame = background.copy()

    for sh in shapes:
        sh.move.apply_move(sh)
        sh.draw(frame)  # sh jumps into the function as 'self' parameter

    cv2.imshow('frame', frame)

    # stop when key pressed
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == 'q':
        break

cv2.destroyAllWindows()
