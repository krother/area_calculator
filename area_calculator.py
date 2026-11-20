"""
Calculate areas of geometrical primitives

front end

could also be called main.py
"""

from workflow import create_workflow
import genai_otel

genai_otel.instrument(
    service_name="langgraph-example",
    enable_prompt_injection_detection=True,  # needs external component -> project idea
)

def main():
    config = {"configurable": {"thread_id": "1"}}
    workflow = create_workflow()
    message = input("describe the shape do you want to calculate the area for: ")
    result = workflow.invoke({"message": message}, config)
    print(result)


if __name__ == "__main__":
    main()
