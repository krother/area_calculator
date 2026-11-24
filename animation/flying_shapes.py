"""
uv add opencv-python
"""
import random
import numpy as np
import cv2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
PURPLE = (192, 0, 192)
BLUE = (192, 0, 0)

MAXX = 1200
MAXY = 800


background = np.zeros((MAXY, MAXX, 3), np.uint8)

x = 128
y = 128
size = 32

def draw_square(frame):
    frame[y:y+size, x:x+size] = GREEN


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


while True:
    frame = background.copy()

    draw_square(frame)
    draw_circle(frame, xcenter=200, ycenter=200)
    draw_triangle(frame, xcenter=800, ycenter=500)

    cv2.imshow('frame', frame)

    # stop when key pressed
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == 'q':
        break

cv2.destroyAllWindows()
