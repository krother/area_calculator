"""
settings that do not justify an environment variable

could load these from a file here
"""
from langgraph.checkpoint.memory import InMemorySaver

CHECKPOINTER = InMemorySaver
