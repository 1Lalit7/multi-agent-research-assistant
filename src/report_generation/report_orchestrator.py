from langgraph.constants import Send
from langchain_core.messages import HumanMessage

from src.report_generation.report_schema import ResearchGraphState
from src.utils.logger import logger

def initiate_all_interviews(state: ResearchGraphState):
    """ This is the "map" step where we run each interview sub-graph using Send API """

    logger.info("Conducting interviews...")

    # Check if human feedback
    human_analyst_feedback=state.get('human_analyst_feedback')
    if human_analyst_feedback:
        # Return to create_analysts
        return "create_analysts"

    # Otherwise kick off interviews in parallel via Send() API
    else:
        topic = state["topic"]
        interview_results = [Send("conduct_interview", {"analyst": analyst,
                                        "messages": [HumanMessage(
                                        content=f"So you said you were writing an article on {topic}?"
                                        )
                                        ]}) for analyst in state["analysts"]]
        
        logger.info("Interviews conducted successfully")

        return interview_results
    

def finalize_report(state: ResearchGraphState):
    """ The is the "reduce" step where we gather all the sections, combine them, and reflect on them to write the intro/conclusion """
    logger.info("Finalizing report...")
    # Save full final report
    content = state["content"]
    if content.startswith("## Insights"):
        content = content.strip("## Insights")
    if "## Sources" in content:
        try:
            content, sources = content.split("\n## Sources\n")
        except:
            sources = None
    else:
        sources = None

    final_report = state["introduction"] + "\n\n---\n\n" + content + "\n\n---\n\n" + state["conclusion"]
    if sources is not None:
        final_report += "\n\n## Sources\n" + sources
    logger.info("Report finalized successfully")
    return {"final_report": final_report} 