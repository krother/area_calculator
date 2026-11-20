"""
pydantic classes that are used to pass data around
so that the different modules can communicate.

sometimes called dto.py (data objects)
"""
from pydantic import BaseModel, Field

from core import Shape


class ShapeRequest(BaseModel):
    name: Shape = Field(description="type of shape")
    size: int = Field(description="edge length or radius")
