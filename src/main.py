"""
Main entry point for the Research Assistant.

This script demonstrates how to use the Research Assistant.
"""

import asyncio
import argparse
import traceback
from src.agents.research_assistant import ResearchAssistant
from src.config.settings import AZURE_OPENAI_API_KEY, TAVILY_API_KEY
from src.utils.helpers import (
    set_env_var, 
    is_empty
)
from src.utils.logger import (
    print_section_header,
    print_success,
    print_error,
    print_warning,
    print_info,
    logger,
    Colors
)

from src.config.default_settings import (
    DEFAULT_RESEARCH_TOPIC,
    DEFAULT_NUM_ANALYSTS,
    DEFAULT_MAX_INTERVIEW_TURNS,
    DEFAULT_OUTPUT_FILE
)

async def main():
    """Main entry point for the Research Assistant."""
    
    # Print welcome message
    print_section_header("MULTI-AGENT RESEARCH ASSISTANT")
    print_info("Welcome to the Multi-Agent Research Assistant!")
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Research Assistant')
    parser.add_argument('--topic', type=str, default=DEFAULT_RESEARCH_TOPIC,
                        help='Research topic')
    parser.add_argument('--analysts', type=int, default=DEFAULT_NUM_ANALYSTS,
                        help='Number of analysts to generate')
    parser.add_argument('--turns', type=int, default=DEFAULT_MAX_INTERVIEW_TURNS,
                        help='Maximum number of conversation turns per interview')
    parser.add_argument('--output', type=str, default=DEFAULT_OUTPUT_FILE,
                        help='Output file for the research report')
    args = parser.parse_args()
    
    # Log the configuration
    logger.info(f"Research topic: {args.topic}")
    logger.info(f"Number of analysts: {args.analysts}")
    logger.info(f"Max interview turns: {args.turns}")
    logger.info(f"Output file: {args.output}")
    
    # Set environment variables if not set
    set_env_var("AZURE_OPENAI_API_KEY", AZURE_OPENAI_API_KEY)
    set_env_var("TAVILY_API_KEY", TAVILY_API_KEY)
    
    # Initialize the research assistant
    assistant = ResearchAssistant()
    assistant.set_topic(args.topic, args.analysts, args.turns)
    
    # Run the entire research process
    report = await assistant.run_research_process(args.output)
    
    # Check if report is empty
    if is_empty(report):
        print_warning("No report content was generated.")
        logger.warning("Empty report generated")
    else:
        # Print report (truncated if very long)
        if len(report) > 500:
            print(f"\n{Colors.MAGENTA}Report Preview:{Colors.RESET}")
            print(f"{report[:500]}...\n{Colors.BRIGHT_BLACK}(Truncated - see full report in {args.output}){Colors.RESET}")
        else:
            print(f"\n{Colors.MAGENTA}Generated Report:{Colors.RESET}")
            print(report)
    if report:
        print_section_header("RESEARCH COMPLETE")
        print_success(f"Research process completed! Report saved to {args.output}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_info("\nResearch process interrupted by user. Exiting...")
    except Exception as e:
        logger.error(f"Error in research process: {str(e)}")
        print(f"{Colors.RED}{Colors.BOLD}An error occurred: {str(e)}{Colors.RESET}")
        raise 