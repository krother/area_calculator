"""Repository that isolates shape persistence from the rest of the program."""
from abc import ABC, abstractmethod

import duckdb

from models import SHAPE_CLASSES, Shape


class ShapeRepositoryError(Exception):
    """Raised when shapes cannot be stored or loaded."""


class ShapeRepository(ABC):
    """Interface that every shape database has to implement."""

    @abstractmethod
    def save_all(self, shapes: list[Shape]) -> None:
        """Replace all stored shapes by the given shapes."""

    @abstractmethod
    def load_all(self) -> list[Shape]:
        """Return all stored shapes in their original order."""


class DuckDBShapeRepository(ShapeRepository):
    """Stores shapes in a DuckDB file as (id, kind, data as JSON)."""

    def __init__(self, path: str) -> None:
        """Open the database and make sure the table exists."""
        try:
            self._con = duckdb.connect(path)
            self._con.execute(
                "CREATE TABLE IF NOT EXISTS shapes "
                "(id INTEGER PRIMARY KEY, kind VARCHAR, data VARCHAR)"
            )
        except duckdb.Error as err:
            raise ShapeRepositoryError(f"cannot open {path}: {err}") from err

    def save_all(self, shapes: list[Shape]) -> None:
        """Replace all stored shapes by the given shapes."""
        rows = [
            (i, type(sh).__name__, sh.model_dump_json())
            for i, sh in enumerate(shapes)
        ]
        try:
            self._con.execute("BEGIN")
            self._con.execute("DELETE FROM shapes")
            if rows:
                self._con.executemany("INSERT INTO shapes VALUES (?, ?, ?)", rows)
            self._con.execute("COMMIT")
        except duckdb.Error as err:
            self._con.execute("ROLLBACK")
            raise ShapeRepositoryError(f"cannot save shapes: {err}") from err

    def load_all(self) -> list[Shape]:
        """Return all stored shapes in their original order."""
        try:
            rows = self._con.execute(
                "SELECT kind, data FROM shapes ORDER BY id"
            ).fetchall()
        except duckdb.Error as err:
            raise ShapeRepositoryError(f"cannot load shapes: {err}") from err
        return [self._to_shape(kind, data) for kind, data in rows]

    @staticmethod
    def _to_shape(kind: str, data: str) -> Shape:
        """Rebuild a shape object from a database row."""
        if kind not in SHAPE_CLASSES:
            raise ShapeRepositoryError(f"unknown shape kind: {kind}")
        return SHAPE_CLASSES[kind].model_validate_json(data)

    def close(self) -> None:
        """Close the database connection."""
        self._con.close()

# penguin
