
import json
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from opentelemetry import trace

from schema import ShapeRequest
from core import MathFunctions, calculate_shape_area
from language_model import call_model
from config import CHECKPOINTER
from repository import save_result



class SimpleMathFunctions(MathFunctions):  # <-- subclass
    """implement the interface required by core"""
    # TODO: move somewhere else

    def lookup_pi(self) -> float:
        return 3.141529

    def sqrt(self, x: float) -> float:
        return x ** 0.5


class MathMathFunctions(MathFunctions):
    """implement the interface required by core"""
    # TODO: move somewhere else

    def lookup_pi(self) -> float:
        return math.pi

    def sqrt(self, x: float) -> float:
        return math.sqrt(x)



class State(TypedDict, total=False):
    message: str
    request: ShapeRequest
    area: float
    file_id: str

"""
HOW TO ADD A DECORATOR FOR OPEN TELEMETRY

def otel(f: Callable):
    # TODO: place in a telemetry.py module

    def wrapper(state):
        ... # do trace stuff here
        result = f(state)
        ... # do more trace stuff here
        return result

    return wrapper

from telemetry import otel

@otel
def calc_area(state: State) -> State:
    ...

"""

def calc_area(state: State) -> State:
    # add some extra info to the trace
    span = trace.get_current_span()  # I want to start a new span (unit of logging)

    # Attach selected state to the current span
    span.set_attribute(
        "langgraph.state.input",
        json.dumps(state, default=str)  # works because state is small!!
    )

    assert "request" in state, "no shape info"  # defensive
    area = calculate_shape_area(state["request"].name,
                                state["request"].size,
                                math_funcs=SimpleMathFunctions() # <-- Dependency Inversion
                                )
    result = {"area": area}

    span.set_attribute(
        "langgraph.state.output",
        json.dumps(result, default=str)
    )
    return result
    

def extract_request(state: State) -> State:
    result = call_model(
        system_prompt = f"Extract a shape calculation request:\n\n",
        user_prompt = state['message']  # type: ignore
    )
    return {"request": result}


def record(state: State) -> State:
    """save the result"""
    id = save_result(
        request = state["request"],
        area = state["area"]
    )
    return {"file_id": id}


def create_workflow():
    graph = StateGraph(State)
    graph.add_node(extract_request)
    graph.add_node(calc_area)  # if using a decorator
    # alternative:
    # graph.add_node(otel_wrapper(calc_area))  # <-- tracer should be defined here (wrapper function)
    graph.add_node(record)

    graph.add_edge(START, "extract_request")
    graph.add_edge("extract_request", "calc_area")
    graph.add_edge("calc_area", "record")
    graph.add_edge("record", END)

    return graph.compile(checkpointer=CHECKPOINTER())
