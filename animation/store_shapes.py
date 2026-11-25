"""Generate the shapes and store them in the database."""
import random

from models import (
    BLUE,
    GREEN,
    ORANGE,
    PURPLE,
    Circle,
    Donut,
    Move,
    Shape,
    Square,
    Triangle,
)
from repository import DuckDBShapeRepository, ShapeRepository

DB_PATH = "shapes.duckdb"


def create_shapes(count: int = 100) -> list[Shape]:
    """Build the fixed shapes plus a number of random squares."""
    shapes: list[Shape] = [
        Donut(x=500, y=500, radius=100, inner_radius=50, color=ORANGE,
              move=Move(scale_mod=1)),
        Square(size=32, color=GREEN, move=Move(xspeed=1, scale_mod=2)),
        Square(x=900, y=400, size=32),
        Circle(x=200, y=200, radius=64, color=PURPLE, move=Move(yspeed=1)),
        Triangle(x=800, y=500, edge_length=50, color=BLUE, direction=1,
                 move=Move(xspeed=-1, yspeed=-1, color_mod=(0, 0, 1))),
        Triangle.blue_upsidedown_triangle(50, 50),
    ]
    for _ in range(count):
        shapes.append(Square(
            x=600, y=400, size=random.randint(5, 20),
            color=(random.randint(50, 255), random.randint(50, 255),
                   random.randint(50, 255)),
            move=Move(xspeed=random.randint(-5, 5),
                      yspeed=random.randint(-5, 5)),
        ))
    return shapes


def store_shapes(repo: ShapeRepository, shapes: list[Shape]) -> None:
    """Save the shapes using the given repository."""
    repo.save_all(shapes)


def main() -> None:
    """Create shapes and store them in the DuckDB file."""
    repo = DuckDBShapeRepository(DB_PATH)
    shapes = create_shapes()
    store_shapes(repo, shapes)
    repo.close()
    print(f"stored {len(shapes)} shapes in {DB_PATH}")


if __name__ == "__main__":
    main()

# penguin
