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


class Square(BaseModel):
    # TODO: forbid extra fields with pydantic config option

    # attributes
    x: int = 128
    y: int = 128
    size: int
    color: Color = BLUE
    # good idea if data does not change: size:int = Field(default=32, gt=0, le=min(MAXX, MAXY))

    def draw(self, frame):
        """
        method: a function inside a class
        self: a reference to the object we are currently working on
        """
        frame[self.y:self.y+self.size,
              self.x:self.x+self.size] = self.color


class Circle(BaseModel):
    x: int
    y: int
    radius: int
    color: Color

    def _draw_circle(self, radius, color):
        Y, X = np.ogrid[0:MAXY, 0:MAXX]
        square_dist = (X - self.x) ** 2 + (Y - self.y) ** 2
        mask = square_dist < radius ** 2
        frame[mask] = color

    def draw(self, frame):
        self._draw_circle(self.radius, self.color)


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


# TODO: create a Shape class that is a superclass of all other shapes
#       attributes: x, y, color
class Triangle(BaseModel):
    x: int
    y: int
    edge_length: int
    color: Color
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

# class: abstraction, instance: concrete object
# table: abstraction, row: concrete data

shapes = [
    Donut(x=500, y=500, radius=100, inner_radius=50, color=ORANGE),
    # TODO explain later why
    Square(size=32, color=GREEN),
    Square(x=900, y=400, size=32),
    Circle(x=200, y=200, radius=64, color=PURPLE),
    Triangle(x=800, y=500, edge_length=50, color=BLUE, direction=-1),
]


background = np.zeros((MAXY, MAXX, 3), np.uint8)

while True:
    frame = background.copy()

    # TODO: make this go away
    shapes[0].x += 2
    shapes[0].y += 1
    #shapes[0].size += 1
    
    shapes[1].x -= 1
    shapes[2].x += 1


    for sh in shapes:
        sh.draw(frame)  # sh jumps into the function as 'self' parameter

    cv2.imshow('frame', frame)

    # stop when key pressed
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == 'q':
        break

cv2.destroyAllWindows()
