from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

from src.report_generation.report_schema import ResearchGraphState
from src.analysts.analyst_generator import create_analysts, human_feedback
from src.report_generation.report_content_generator import write_introduction, write_conclusion, write_report
from src.report_generation.report_orchestrator import finalize_report, initiate_all_interviews
from src.interview.interview_graph import build_interview_graph


def build_report_generator():
    # Add nodes and edges
    builder = StateGraph(ResearchGraphState)
    builder.add_node("create_analysts", create_analysts)
    builder.add_node("human_feedback", human_feedback)
    builder.add_node("conduct_interview", build_interview_graph())
    builder.add_node("write_report", write_report)
    builder.add_node("write_introduction", write_introduction)
    builder.add_node("write_conclusion", write_conclusion)
    builder.add_node("finalize_report", finalize_report)

    # Logic
    builder.add_edge(START, "create_analysts")
    builder.add_edge("create_analysts", "human_feedback")
    builder.add_conditional_edges("human_feedback", initiate_all_interviews, ["create_analysts", "conduct_interview"])
    builder.add_edge("conduct_interview", "write_report")
    builder.add_edge("conduct_interview", "write_introduction")
    builder.add_edge("conduct_interview", "write_conclusion")
    builder.add_edge(["write_conclusion", "write_report", "write_introduction"], "finalize_report")
    builder.add_edge("finalize_report", END)

    # Compile
    memory = MemorySaver()
    return builder.compile(interrupt_before=['human_feedback'], checkpointer=memory) 