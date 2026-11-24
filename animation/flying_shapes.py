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

MAXX = 1200
MAXY = 800


class Square(BaseModel):
    # TODO: forbid extra fields with pydantic config option

    # attributes
    x: int
    y: int
    size: int
    color: tuple[int, int, int]



def draw_square(frame, square: Square):
    frame[square.y:square.y+square.size,
          square.x:square.x+square.size] = square.color


def draw_circle(frame, xcenter, ycenter):
    radius = 64
    Y, X = np.ogrid[0:MAXY, 0:MAXX]
    square_dist = (X - xcenter) ** 2 + (Y - ycenter) ** 2
    mask = square_dist < radius ** 2
    frame[mask] = PURPLE


def draw_triangle(frame, xcenter, ycenter, side=64, direction=1):
    """Draw an upright equilateral triangle. Direction is -1/1."""
    height = side * np.sqrt(3) / 2
    points = np.array([
        [xcenter, ycenter - direction * 2 * height / 3],
        [xcenter - side / 2, ycenter + direction * height / 3],
        [xcenter + side / 2, ycenter + direction * height / 3],
    ])
    cv2.fillPoly(frame, [np.round(points).astype(np.int32)], BLUE)

# class: abstraction, instance: concrete object
# table: abstraction, row: concrete data

squares = [
    Square(x=128, y=128, size=32, color=GREEN),  # instance <- class
    Square(x=900, y=400, size=32, color=BLUE),
]

circlex, circley = 200, 200

background = np.zeros((MAXY, MAXX, 3), np.uint8)

while True:
    frame = background.copy()

    squares[0].x += 2
    squares[0].y += 1
    squares[0].size += 1
    
    squares[1].x -= 1

    circlex += 1

    for sq in squares:
        draw_square(frame, sq)

    draw_circle(frame, xcenter=circlex, ycenter=circley)
    draw_triangle(frame, xcenter=800, ycenter=500)

    cv2.imshow('frame', frame)

    # stop when key pressed
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == 'q':
        break

cv2.destroyAllWindows()
