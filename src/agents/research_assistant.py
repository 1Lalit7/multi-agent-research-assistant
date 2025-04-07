"""
Research Assistant - Main coordinator for the research process.

This module orchestrates the entire research process from analyst generation
to conducting interviews in parallel to producing the final report using an integrated workflow.
"""

import traceback
from typing import Dict, List, Any, Optional

# Import the integrated report generator instead of individual components
from src.report_generation.report_generation_graph import build_report_generator
from src.config.default_settings import (
    DEFAULT_MAX_INTERVIEW_TURNS, 
    DEFAULT_NUM_ANALYSTS, 
    DEFAULT_RESEARCH_TOPIC,
    DEFAULT_OUTPUT_FILE
)
from src.utils.helpers import (
    display_analyst, 
    save_report_to_file
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

class ResearchAssistant:
    """
    Research Assistant that orchestrates the entire research process.
    """
    
    def __init__(self):
        """Initialize the research assistant components."""
        logger.info("Initializing Research Assistant")
        try:
            # Build the integrated report generator graph
            self.report_graph = build_report_generator()
            
            # Store state for running the research process
            self.analysts = []
            self.topic = ""
            self.max_analysts = DEFAULT_NUM_ANALYSTS
            self.max_interview_turns = DEFAULT_MAX_INTERVIEW_TURNS
            self.sections = []
            self.final_report = ""
            self.thread = {"configurable": {"thread_id": "main_workflow"}}
            logger.debug("Research Assistant initialized")
        except Exception as e:
            logger.error(f"Error initializing Research Assistant: {str(e)}")
            print_error(f"Failed to initialize Research Assistant: {str(e)}")
            traceback.print_exc()
            raise
        
    def set_topic(self, 
                    topic: str = DEFAULT_RESEARCH_TOPIC, 
                    max_analysts: int = DEFAULT_NUM_ANALYSTS, 
                    max_interview_turns: int = DEFAULT_MAX_INTERVIEW_TURNS):
        """
        Set the research topic and parameters.
        
        Args:
            topic: The research topic
            max_analysts: Maximum number of analysts to generate
            max_interview_turns: Maximum turns for each interview
            
        Returns:
            None
        """
        logger.info(f"Setting research topic: '{topic}'")
        self.topic = topic
        self.max_analysts = max_analysts
        self.max_interview_turns = max_interview_turns
        
    def generate_analysts(self):
        """
        Generate analysts based on the topic.
        
        Returns:
            List of generated analysts
        """
        print_section_header(f"GENERATING ANALYSTS FOR '{self.topic}'")
        logger.info("Starting analyst generation")
        
        try:
            # Initialize the graph with topic and max_analysts
            initial_state = {
                "topic": self.topic,
                "max_analysts": self.max_analysts,
                "max_num_turns": self.max_interview_turns
            }
            
            logger.debug(f"Initial state: {initial_state}")
            
            # Run the graph until analyst generation is complete
            for event in self.report_graph.stream(
                initial_state,
                self.thread,
                stream_mode="values"
            ):
                # Log received events for debugging
                logger.debug(f"Received event with keys: {list(event.keys())}")
                
                # Retrieve generated analysts
                analysts = event.get('analysts', [])
                if analysts:
                    # Display the analysts
                    print_section_header(f"GENERATED ANALYSTS FOR '{self.topic}'")
                    for analyst in analysts:
                        display_analyst(analyst.dict())
                    
                    # Store the analysts
                    self.analysts = analysts
                    logger.info(f"Generated {len(analysts)} analysts")
                    # Break the stream after analysts are generated
                    break
            
            return self.analysts
        except Exception as e:
            error_msg = f"Error generating analysts: {str(e)}"
            logger.error(error_msg)
            print_error(error_msg)
            traceback.print_exc()
            return []
    
    def provide_feedback(self, feedback: str):
        """
        Provide feedback on the generated analysts.
        
        Args:
            feedback: User feedback on the analysts
            
        Returns:
            List of updated analysts
        """
        print_section_header("REFINING ANALYSTS BASED ON FEEDBACK")
        logger.info("Processing feedback on analysts")
        
        try:
            # Update state with feedback
            self.report_graph.update_state(
                self.thread, 
                {"human_analyst_feedback": feedback}, 
                as_node="human_feedback"
            )
            
            # Continue execution
            for event in self.report_graph.stream(
                None, 
                self.thread, 
                stream_mode="values"
            ):
                # Log received events for debugging
                logger.debug(f"Feedback event with keys: {list(event.keys())}")
                
                # Retrieve updated analysts
                analysts = event.get('analysts', [])
                if analysts:
                    # Display the updated analysts
                    print_section_header("UPDATED ANALYSTS BASED ON FEEDBACK")
                    for analyst in analysts:
                        display_analyst(analyst.dict())
                    
                    # Store the updated analysts
                    self.analysts = analysts
                    logger.info(f"Updated {len(analysts)} analysts based on feedback")
                    # Break the stream after analysts are updated
                    break
            
            return self.analysts
        except Exception as e:
            error_msg = f"Error processing feedback: {str(e)}"
            logger.error(error_msg)
            print_error(error_msg)
            traceback.print_exc()
            return self.analysts
    
    async def conduct_interviews_and_generate_report(self, output_file: str = DEFAULT_OUTPUT_FILE) -> Optional[str]:
        """
        Continue the workflow to conduct interviews and generate the final report.
        
        Args:
            output_file: File to save the report to
            
        Returns:
            The generated report or None if there was an error
        """
        if not self.analysts:
            print_error("No analysts available. Please generate analysts first.")
            logger.error("Attempted to conduct interviews with no analysts")
            return None
        
        print_section_header("CONDUCTING INTERVIEWS AND GENERATING REPORT")
        logger.info("Starting interview and report generation process")
        
        logger.info("Interview is in progress...")
        try:
            # Continue the workflow (which will handle the interviews and report generation)
            for event in self.report_graph.stream(
                None, 
                self.thread, 
                stream_mode="values"
            ):
                # Log the event keys for debugging
                logger.debug(f"Interview event with keys: {list(event.keys())}")
                
                # Print updates about the progress
                if event.get("sections"):
                    print_success("Interview section completed")
                    logger.debug(f"Section content: {event.get('sections')[:100]}...")
                
                # Debug logging for other important steps
                if event.get("introduction"):
                    print_info("Report introduction generated")
                
                if event.get("content"):
                    logger.debug("Content generated")
                    print_info("Report body generated")
                    
                if event.get("conclusion"):
                    logger.debug("Conclusion generated")
                    print_info("Report conclusion generated")
                
                # Check for final report
                if event.get("final_report"):
                    final_report = event.get("final_report")
                    if final_report is not None:
                        logger.info("Generating final report...")
                    logger.debug(f"Final report received. Length: {len(final_report)} characters")
                    
                    if not final_report or final_report.strip() == "":
                        logger.warning("Empty report received")
                        print_warning("Empty report generated!")
                        return None
                        
                    self.final_report = final_report
                    
                    # Save to file
                    logger.info("Saving report to file...")
                    save_report_to_file(final_report, output_file)
                    # print_section_header(f"RESEARCH COMPLETE")
                    # print_success(f"Final report generated and saved to {output_file}")
                    # logger.info(f"Research process completed successfully")
                    return final_report
            
            # If we reached here, we didn't get a final report
            logger.warning("No final report event received")
            print_warning("No final report was generated by the workflow")
            return None
            
        except Exception as e:
            error_msg = f"Error in interview and report generation: {str(e)}"
            logger.error(error_msg)
            print_error(error_msg)
            traceback.print_exc()
            return None
    
    async def run_research_process(self, output_file: str = DEFAULT_OUTPUT_FILE) -> Optional[str]:
        """
        Run the full research process from analyst generation to final report.
        
        Args:
            output_file: File to save the report to
            
        Returns:
            The generated report or None if there was an error
        """
        logger.info("Starting full research process")
        
        try:
            # Generate analysts
            self.generate_analysts()
            
            if not self.analysts:
                print_error("Failed to generate analysts. Cannot continue.")
                return None
            
            # Ask for feedback
            while True:
                feedback = input(f"\n{Colors.YELLOW}Do you want to provide feedback on the analysts? (y/n): {Colors.RESET}")
                if feedback.lower() == 'y':
                    feedback_text = input(f"{Colors.CYAN}Please provide your feedback: {Colors.RESET}")
                    self.provide_feedback(feedback_text)
                elif feedback.lower() == 'n':
                    print_info("Proceeding without additional feedback")
                    break
                else:
                    print_warning("Invalid input. Please enter 'y' or 'n'.")
            
            # Conduct interviews and generate report
            report = await self.conduct_interviews_and_generate_report(output_file)
            return report
            
        except Exception as e:
            error_msg = f"Error in research process: {str(e)}"
            logger.error(error_msg)
            print_error(error_msg)
            traceback.print_exc()
            return None 