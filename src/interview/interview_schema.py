"""
Schema definitions for the interview module.
"""

import operator
from typing import Annotated
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState

from src.analysts.analyst_schema import Analyst

class InterviewState(MessagesState):
    """State for interview between analyst and expert."""
    
    max_num_turns: int  # Number turns of conversation
    context: Annotated[list, operator.add]  # Source docs
    analyst: Analyst  # Analyst asking questions
    interview: str  # Interview transcript
    sections: list  # Final key we duplicate in outer state for Send() API

class SearchQuery(BaseModel):
    """Search query for retrieval."""
    
    search_query: str = Field(None, description="Search query for retrieval.") 