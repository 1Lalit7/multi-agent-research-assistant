"""
Generate analyst questions for interviews.
"""

from typing import Dict, Any
from langchain_core.messages import SystemMessage

from src.models.llm import llm
from src.interview.interview_schema import InterviewState
from src.utils.logger import logger, print_info
from src.prompts.question_prompt import QUESTION_INSTRUCTIONS


def generate_question(state: InterviewState) -> Dict[str, Any]:
    """
    Generate the next question from an analyst.
    
    Args:
        state: The current interview state
        
    Returns:
        Dict with the updated messages
    """
    logger.info("Generating question...")
    # Get state
    analyst = state["analyst"]
    messages = state["messages"]

    # Generate question based on the analyst's persona
    system_message = QUESTION_INSTRUCTIONS.format(goals=analyst.persona)
    question = llm.invoke([SystemMessage(content=system_message)] + messages)

    print_info(f"Question: \n{question.content}")

    logger.info("Question Generated Successfully")

    # Write messages to state
    return {"messages": [question]} 