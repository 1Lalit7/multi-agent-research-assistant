"""
Configuration settings for the research assistant system.

This module manages environment variables and global configuration settings.
"""

import os
from dotenv import load_dotenv
from src.utils.logger import logger, print_warning

# Load environment variables from .env file
load_dotenv()

# API Keys (with empty defaults for safety)
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Tavily API Key
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")


# System paths
SYSTEM_PROMPTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
    "prompts"
)

# # Log configuration settings
# logger.info(f"Using model: {AZURE_OPENAI_DEPLOYMENT or OPENAI_MODEL}")
# logger.info(f"Model temperature: {DEFAULT_MODEL_TEMPERATURE}")
# logger.info(f"Default output file: {DEFAULT_OUTPUT_FILE}")

# Initialize other configuration settings
def init_config():
    """Initialize configuration settings."""
    # Ensure the required API keys are available or will be prompted for
    if not AZURE_OPENAI_API_KEY and not OPENAI_API_KEY:
        warning_msg = "No OpenAI API key found in environment variables. You will be prompted to enter it when needed."
        logger.warning(warning_msg)
        print_warning(warning_msg)
    
    if not TAVILY_API_KEY:
        warning_msg = "No Tavily API key found in environment variables. You will be prompted to enter it when needed."
        logger.warning(warning_msg)
        print_warning(warning_msg)

# Initialize config 
init_config() 