"""
Build the interview graph that connects question generation, search, and answers.
"""

from typing import Dict, Any
from langchain_core.messages import get_buffer_string, AIMessage, HumanMessage, SystemMessage


from src.interview.interview_schema import InterviewState
from src.models.llm import llm
from src.utils.logger import logger, print_info
from src.prompts.section_prompt import SECTION_WRITER_INSTRUCTIONS

def save_transcript(state: InterviewState) -> Dict[str, Any]:
    """
    Save the conversation transcript to state.
    
    Args:
        state: The current interview state
        
    Returns:
        Dict with the interview transcript
    """

    logger.info("Saving Inverview...")

    # Convert messages to a string
    transcript = get_buffer_string(state["messages"])

    logger.info("Inverview Saved Successfully")
    
    # Save transcript
    return {"interview": transcript}


def route_messages(state: InterviewState,
                    name: str = "expert"):

    """ Route between question and answer """

    # Get messages
    messages = state["messages"]
    max_num_turns = state.get('max_num_turns',1)

    # Check the number of expert answers
    num_responses = len(
        [m for m in messages if isinstance(m, AIMessage) and m.name == name]
    )

    # End if expert has answered more than the max turns
    if num_responses >= max_num_turns:
        return 'save_transcript'

    # This router is run after each question - answer pair
    # Get the last question asked to check if it signals the end of discussion
    last_question = messages[-2]

    if "Thank you so much for your help" in last_question.content:
        return 'save_transcript'
    return "ask_question"



def write_section(state: InterviewState):

    """ Node to answer a question """

    logger.info("Writing a section...")

    # Get state
    interview = state["interview"]
    context = state["context"]
    analyst = state["analyst"]

    # Write section using either the gathered source docs from interview (context) or the interview itself (interview)
    system_message = SECTION_WRITER_INSTRUCTIONS.format(focus=analyst.description)
    section = llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content=f"Use this source to write your section: {context}")])

    logger.info("Section is generated successfully")

    # Append it to state
    return {"sections": [section.content]}

