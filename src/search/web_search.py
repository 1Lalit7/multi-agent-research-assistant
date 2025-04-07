"""
Web search functionality for retrieving information.
"""

from typing import Dict, Any
from langchain_core.messages import SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WikipediaLoader

from src.models.llm import llm
from src.interview.interview_schema import InterviewState, SearchQuery
from src.config.settings import TAVILY_API_KEY
from src.utils.logger import logger, print_info
from src.prompts.search_prompt import SEARCH_INSTRUCTIONS
from src.config.default_settings import DEFAULT_N_DOCUMENT_TO_SEARCH

# Initialize search tools
tavily_search = TavilySearchResults(max_results=DEFAULT_N_DOCUMENT_TO_SEARCH)



def search_web(state: InterviewState) -> Dict[str, Any]:
    """
    Retrieve documents from web search based on the conversation.
    
    Args:
        state: The current interview state
        
    Returns:
        Dict with the updated context
    """
    logger.info("Searching web...")
    # Generate search query
    structured_llm = llm.with_structured_output(SearchQuery)
    
    search_query = structured_llm.invoke(
        [SystemMessage(content=SEARCH_INSTRUCTIONS)] + state['messages']
    )
    
    # Perform search
    search_results = tavily_search.invoke(search_query.search_query)
    
    # Format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_results
        ]
    )

    print_info(f"Number of Search results from web: {len(formatted_search_docs)}")

    print_info(f"Search results from web: \n{formatted_search_docs[0:10]}")

    logger.info("Searching web completed successfully")


    return {"context": [formatted_search_docs]}

def search_wikipedia(state: InterviewState) -> Dict[str, Any]:
    """
    Retrieve documents from Wikipedia based on the conversation.
    
    Args:
        state: The current interview state
        
    Returns:
        Dict with the updated context
    """
    logger.info("Searching Wikipedia...")
    # Generate search query
    structured_llm = llm.with_structured_output(SearchQuery)
    search_query = structured_llm.invoke(
        [SystemMessage(content=SEARCH_INSTRUCTIONS)] + state['messages']
    )
    
    # Perform Wikipedia search
    wiki_docs = WikipediaLoader(
        query=search_query.search_query,
        load_max_docs=DEFAULT_N_DOCUMENT_TO_SEARCH
    ).load()
    
    # Format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content}\n</Document>'
            for doc in wiki_docs
        ]
    )

    print_info(f"Number of Search results from wikepedia: {len(formatted_search_docs)}")

    print_info(f"Search results from wikepedia: \n{formatted_search_docs[0:10]}")

    logger.info("Searching wikipedia completed successfully")

    return {"context": [formatted_search_docs]}