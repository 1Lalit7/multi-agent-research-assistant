"""
Helper utilities for the research assistant.
"""

import os
import getpass
from typing import Dict, Any, Optional

from src.utils.logger import (
    logger,
    Colors,
    print_success,
    print_error
)

def set_env_var(var_name: str, default_value: Optional[str] = None) -> None:
    """
    Set an environment variable if it doesn't exist.
    
    Args:
        var_name: Name of the environment variable
        default_value: Default value if not set and user doesn't input
        
    Returns:
        None
    """
    if not os.environ.get(var_name):
        if default_value:
            os.environ[var_name] = default_value
            logger.info(f"Set {var_name} with default value")
        else:
            os.environ[var_name] = getpass.getpass(f"{var_name}: ")
            logger.info(f"Set {var_name} from user input")
            
def display_analyst(analyst: Dict[str, Any]) -> None:
    """
    Display analyst information in a formatted way.
    
    Args:
        analyst: Dictionary containing analyst information
        
    Returns:
        None
    """
    print(f"{Colors.BOLD}{Colors.CYAN}Name:{Colors.RESET} {analyst['name']}")
    print(f"{Colors.BOLD}{Colors.CYAN}Affiliation:{Colors.RESET} {analyst['affiliation']}")
    print(f"{Colors.BOLD}{Colors.CYAN}Role:{Colors.RESET} {analyst['role']}")
    print(f"{Colors.BOLD}{Colors.CYAN}Description:{Colors.RESET} {analyst['description']}")
    print(f"{Colors.BRIGHT_BLACK}{'-' * 50}{Colors.RESET}")
    

    
def save_report_to_file(report: str, filename: str = "research_report.md") -> None:
    """
    Save a generated report to a markdown file.
    
    Args:
        report: The generated report text
        filename: Name of the file to save to
        
    Returns:
        None
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        
        logger.info(f"Report saved to {filename} file successfully")
        print_success(f"Report saved to {filename} file successfully")
    except Exception as e:
        error_msg = f"Error saving report to file {filename}: {str(e)}"
        logger.error(error_msg)
        print_error(error_msg)

# Function to check if a string is empty or None
def is_empty(text: Optional[str]) -> bool:
    """Check if a string is empty or None."""
    return text is None or text.strip() == ""

if __name__ == "__main__":
    print_success("Helper utilities test!")
    save_report_to_file("Test report content", "test_report.md")
