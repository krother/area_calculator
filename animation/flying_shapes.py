"""Load shapes from the database and display them as an animation.

Run store_shapes.py first.
"""
import cv2
import numpy as np

from models import MAXX, MAXY, Shape
from repository import DuckDBShapeRepository, ShapeRepository
from store_shapes import DB_PATH


def animate_step(shapes: list[Shape], background: np.ndarray) -> np.ndarray:
    """Move all shapes one step and return the drawn frame."""
    frame = background.copy()
    for sh in shapes:
        sh.move.apply_move(sh)
        sh.draw(frame)
    return frame


def run(repo: ShapeRepository) -> None:
    """Show the animation until 'q' is pressed."""
    shapes = repo.load_all()
    background = np.zeros((MAXY, MAXX, 3), np.uint8)
    while True:
        cv2.imshow('frame', animate_step(shapes, background))
        if chr(cv2.waitKey(1) & 0xFF) == 'q':
            break
    cv2.destroyAllWindows()


def main() -> None:
    """Open the database and start the animation."""
    repo = DuckDBShapeRepository(DB_PATH)
    run(repo)
    repo.close()


if __name__ == "__main__":
    main()

# penguin
