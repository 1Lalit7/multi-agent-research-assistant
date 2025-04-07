"""
Analyst Generator Module

Responsible for generating diverse analyst personas based on a research topic.
Uses LangGraph to create a flow that generates, evaluates, and refines analyst profiles.
"""

from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

from src.models.llm import llm
from src.analysts.analyst_schema import Perspectives, GenerateAnalystsState
from src.utils.helpers import display_analyst
from src.utils.logger import logger
from src.prompts.analyst_prompt import ANALYST_INSTRUCTIONS




def create_analysts(state: GenerateAnalystsState) -> Dict[str, Any]:
    """
    Create analyst personas based on a research topic.
    
    Args:
        state: The current state with topic and constraints
        
    Returns:
        Dict with analysts list
    """

    logger.info("Generating analysts...")
    topic = state['topic']
    max_analysts = state['max_analysts']
    human_analyst_feedback = state.get('human_analyst_feedback', '')

    # Enforce structured output
    structured_llm = llm.with_structured_output(Perspectives)

    # System message
    system_message = ANALYST_INSTRUCTIONS.format(
        topic=topic,
        human_analyst_feedback=human_analyst_feedback,
        max_analysts=max_analysts
    )

    # Generate analysts
    analysts = structured_llm.invoke(
        [SystemMessage(content=system_message)] + 
        [HumanMessage(content="Generate the set of analysts.")]
    )

    logger.info("Analysts generated successfully")

    # Return the list of analysts
    return {"analysts": analysts.analysts}

def human_feedback(state: GenerateAnalystsState):
    """
    No-op node that should be interrupted on.
    This is where human feedback would be incorporated.
    """
    pass

def should_continue(state: GenerateAnalystsState):
    """
    Determine the next node to execute based on presence of human feedback.
    
    Args:
        state: The current state
        
    Returns:
        String indicating the next node or END
    """
    # Check if human feedback exists
    human_analyst_feedback = state.get('human_analyst_feedback', None)
    if human_analyst_feedback:
        return "create_analysts"

    # Otherwise end
    return END

def build_analyst_generator():
    """
    Build and return the analyst generation graph.
    
    Returns:
        StateGraph: The compiled graph for analyst generation
    """
    # Add nodes and edges
    builder = StateGraph(GenerateAnalystsState)
    builder.add_node("create_analysts", create_analysts)
    builder.add_node("human_feedback", human_feedback)
    
    builder.add_edge(START, "create_analysts")
    builder.add_edge("create_analysts", "human_feedback")
    builder.add_conditional_edges(
        "human_feedback", 
        should_continue, 
        ["create_analysts", END]
    )

    # Compile with interruption point
    memory = MemorySaver()
    return builder.compile(
        interrupt_before=['human_feedback'], 
        checkpointer=memory
    ) 


if __name__ == "__main__":
    # from IPython.display import Image, display

    graph = build_analyst_generator()

    # display(Image(graph.get_graph(xray=1).draw_mermaid_png()))

    # Input
    max_analysts = 2
    topic = "The benefits of ai agents"
    thread = {"configurable": {"thread_id": "1"}}

    # Run the graph until the first interruption
    for event in graph.stream({"topic":topic,"max_analysts":max_analysts,}, thread, stream_mode="values"):
        # Review
        analysts = event.get('analysts', '')
        if analysts:
            print(f"\n=== Generated Analysts ===\n")
            for analyst in analysts:
                display_analyst(analyst.dict())

    while True:
        user_input = input("Do you want to provide the feedback - y/n: ")
        if user_input.lower() == "y":
            feedback = input("Provide feedback to improve the analyst: ")

            graph.update_state(thread, {"human_analyst_feedback": feedback}, as_node="human_feedback")

            for event in graph.stream(None, thread, stream_mode="values"):
                # Review
                analysts = event.get('analysts', '')
                if analysts:
                    print(f"\n=== Updated Generated Analysts ===\n")
                    for analyst in analysts:
                        display_analyst(analyst.dict())
        elif user_input.lower() == "n":
            break
        else:
            print(f"Enter the valid user input - y/n")

