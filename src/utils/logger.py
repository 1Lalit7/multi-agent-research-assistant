"""
Logging utilities for the research assistant.

This module provides colored logging functionality and terminal color constants.
"""

import logging

# ANSI color codes for colorful terminal output
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

def configure_logging():
    """Configure colorful logging."""
    # Create a custom formatter with colors
    class ColoredFormatter(logging.Formatter):
        format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        FORMATS = {
            logging.DEBUG: Colors.BLUE + format_str + Colors.RESET,
            logging.INFO: Colors.GREEN + format_str + Colors.RESET,
            logging.WARNING: Colors.YELLOW + format_str + Colors.RESET,
            logging.ERROR: Colors.RED + format_str + Colors.RESET,
            logging.CRITICAL: Colors.BG_RED + Colors.WHITE + format_str + Colors.RESET
        }
        
        def format(self, record):
            log_format = self.FORMATS.get(record.levelno, self.format_str)
            formatter = logging.Formatter(log_format)
            return formatter.format(record)
    
    # Create logger
    logger = logging.getLogger("Research Assistant")
    logger.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter())
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger

# Initialize the logger
logger = configure_logging()

def print_section_header(text: str) -> None:
    """
    Print a colorful section header.
    
    Args:
        text: The header text
        
    Returns:
        None
    """
    print(f"\n{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD} {text} {Colors.RESET}\n")
    
def print_success(text: str) -> None:
    """
    Print a success message.
    
    Args:
        text: The success message
        
    Returns:
        None
    """
    print(f"{Colors.GREEN}{Colors.BOLD}{text}{Colors.RESET}")
    
def print_error(text: str) -> None:
    """
    Print an error message.
    
    Args:
        text: The error message
        
    Returns:
        None
    """
    print(f"{Colors.RED}{Colors.BOLD}{text}{Colors.RESET}")
    
def print_warning(text: str) -> None:
    """
    Print a warning message.
    
    Args:
        text: The warning message
        
    Returns:
        None
    """
    print(f"{Colors.YELLOW}{Colors.BOLD}{text}{Colors.RESET}")
    
def print_info(text: str) -> None:
    """
    Print an info message.
    
    Args:
        text: The info message
        
    Returns:
        None
    """
    print(f"{Colors.BLUE}{text}{Colors.RESET}")

if __name__ == "__main__":
    print_success("Logger test: success")
    print_error("Logger test: error")
    print_warning("Logger test: warning")
    print_info("Logger test: info")
    print_section_header("Logger test: header")
    
    logger.debug("Logger test: debug message")
    logger.info("Logger test: info message")
    logger.warning("Logger test: warning message")
    logger.error("Logger test: error message")
    logger.critical("Logger test: critical message") 