
from langchain_ollama import ChatOllama

from schema import ShapeRequest

def call_model(user_prompt: str, system_prompt: str):
    """use Ollama to extract info on geometrical shape"""
    llm = ChatOllama(model="qwen3:0.6b", temperature=0)
    classifier = llm.with_structured_output(ShapeRequest)
    result = classifier.invoke(system_prompt + "\n" + user_prompt)
    return result

    # TODO: in tests, you want to patch/mock this function
