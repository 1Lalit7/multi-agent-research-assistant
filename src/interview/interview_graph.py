
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

from src.interview.question_generator import generate_question
from src.search.web_search import search_web, search_wikipedia
from src.interview.answer_generator import generate_answer
from src.interview.interview_schema import InterviewState
from src.interview.interview_components import save_transcript, write_section, route_messages

def build_interview_graph():
    """
    Build and compile the interview graph.
    
    Returns:
        The compiled interview graph
    """
    # Initialize graph builder
    builder = StateGraph(InterviewState)
    
    # Add nodes
    builder.add_node("ask_question", generate_question)
    builder.add_node("search_web", search_web)
    builder.add_node("search_wikipedia", search_wikipedia)
    builder.add_node("answer_question", generate_answer)
    builder.add_node("save_transcript", save_transcript)
    builder.add_node("write_section", write_section)
    
    # Add edges
    builder.add_edge(START, "ask_question")
    builder.add_edge("ask_question", "search_web")
    builder.add_edge("ask_question", "search_wikipedia")
    builder.add_edge("search_web", "answer_question")
    builder.add_edge("search_wikipedia", "answer_question")

    # Conditional branching
    builder.add_conditional_edges("answer_question", route_messages, ['ask_question','save_transcript'])
    
    
    builder.add_edge("save_transcript", "write_section")
    builder.add_edge("write_section", END)
    
    # Compile graph
    memory = MemorySaver()
    return builder.compile(checkpointer=memory) 