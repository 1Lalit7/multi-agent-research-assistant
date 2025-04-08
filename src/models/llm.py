"""
Language model initialization and configuration.
"""

from langchain_openai import AzureChatOpenAI, ChatOpenAI
from src.config.settings import (
    AZURE_OPENAI_ENDPOINT, 
    AZURE_OPENAI_API_KEY, 
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_VERSION,
    OPENAI_API_KEY,
    OPENAI_MODEL
)

from src.config.default_settings import DEFAULT_MODEL_TEMPERATURE


# Initialize the LLM
def initialize_llm():
    """Get the appropriate LLM based on available API keys."""
    if AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT:
        return AzureChatOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            openai_api_key=AZURE_OPENAI_API_KEY,
            openai_api_version=AZURE_OPENAI_API_VERSION,
            model=AZURE_OPENAI_DEPLOYMENT,
            temperature=DEFAULT_MODEL_TEMPERATURE,
            max_retries=5,
            request_timeout=60,
        )
    elif OPENAI_API_KEY:
        return ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=DEFAULT_MODEL_TEMPERATURE,
            api_key=OPENAI_API_KEY,
        )
    else:
        raise ValueError("No OpenAI API key provided. Set AZURE_OPENAI_API_KEY or OPENAI_API_KEY.")

# Create a default instance
llm = initialize_llm() 

if __name__ == "__main__":
    response = llm.invoke("who are you?")
    print(response.content)
