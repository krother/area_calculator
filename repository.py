"""
read/write operations

could use: files, web connections, databases
"""
import uuid
import json

from schema import ShapeRequest

def save_result(request: ShapeRequest, area: float) -> str:
    id = str(uuid.uuid1())
    filename = f"{id}.json"
    j = {
        "id": id,
        "shape": request.name,
        "size": request.size,
        "area": area,
    }
    with open(filename, "w") as f:
        f.write(json.dumps(j))
    return id
