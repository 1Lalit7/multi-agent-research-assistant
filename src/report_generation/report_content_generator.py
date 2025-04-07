from langchain_core.messages import HumanMessage, SystemMessage

from src.report_generation.report_schema import ResearchGraphState
from src.models.llm import llm
from src.utils.logger import logger
from src.prompts.intro_conclusion_prompt import INTRO_CONCLUSTION_INSTRUCTIONS
from src.prompts.report_instruction_prompt import REPORT_WRITER_INSTRUCTIONS




def write_introduction(state: ResearchGraphState):

    logger.info("Writing report introduction...")

    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    # Summarize the sections into a final report

    instructions = INTRO_CONCLUSTION_INSTRUCTIONS.format(topic=topic, formatted_str_sections=formatted_str_sections)
    intro = llm.invoke([instructions]+[HumanMessage(content=f"Write the report introduction")])

    logger.info("Report introduction is written successfully")

    return {"introduction": intro.content}

def write_conclusion(state: ResearchGraphState):

    logger.info("Writing report conclusion...")

    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    # Summarize the sections into a final report

    instructions = INTRO_CONCLUSTION_INSTRUCTIONS.format(topic=topic, formatted_str_sections=formatted_str_sections)
    conclusion = llm.invoke([instructions]+[HumanMessage(content=f"Write the report conclusion")])

    logger.info("Report conclusion is written successfully")

    return {"conclusion": conclusion.content}




def write_report(state: ResearchGraphState):

    logger.info("Writing report body...")
    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    # Summarize the sections into a final report
    system_message = REPORT_WRITER_INSTRUCTIONS.format(topic=topic, context=formatted_str_sections)
    report = llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content=f"Write a report based upon these memos.")])

    logger.info("Report body is written successfully")

    return {"content": report.content} 