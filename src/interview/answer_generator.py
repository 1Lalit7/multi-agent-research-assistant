"""
Expert answer generation based on retrieved context.
"""

from langchain_core.messages import SystemMessage

from src.models.llm import llm
from src.interview.interview_schema import InterviewState
from src.utils.logger import logger, print_info
from src.prompts.answer_prompt import ANSWER_INSTRUCTIONS



def generate_answer(state: InterviewState):

    """ Node to answer a question """

    logger.info("Generating answer...")

    # Get state
    analyst = state["analyst"]
    messages = state["messages"]
    context = state["context"]

    # Answer question
    system_message = ANSWER_INSTRUCTIONS.format(goals=analyst.persona, context=context)
    answer = llm.invoke([SystemMessage(content=system_message)]+messages)

    print_info(f"Answer: \n{answer.content}")
    logger.info("Answer is generated successfully")

    # Name the message as coming from the expert
    answer.name = "expert"

    # Append it to state
    return {"messages": [answer]} 