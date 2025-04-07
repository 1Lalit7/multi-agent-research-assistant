"""
Research Assistant Streamlit Web Application

This module provides a web interface for the research assistant system using Streamlit.
Users can configure settings, run research tasks, and download the generated reports.
"""

import os
import asyncio
import streamlit as st
from datetime import datetime
import time
from typing import Optional

from src.agents.research_assistant import ResearchAssistant
from src.config.settings import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT,
    TAVILY_API_KEY
)

from src.config.default_settings import (
    DEFAULT_MODEL_TEMPERATURE,
    DEFAULT_NUM_ANALYSTS,
    DEFAULT_MAX_INTERVIEW_TURNS,
    DEFAULT_RESEARCH_TOPIC
)

from src.utils.logger import (
    print_info,
    Colors,
    logger
)


from src.utils.helpers import (
    set_env_var
)

# Initialize session state
if 'research_complete' not in st.session_state:
    st.session_state.research_complete = False
if 'report_content' not in st.session_state:
    st.session_state.report_content = ""
if 'report_filename' not in st.session_state:
    st.session_state.report_filename = ""
if 'analysts' not in st.session_state:
    st.session_state.analysts = []
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'status' not in st.session_state:
    st.session_state.status = ""
if 'api_keys_set' not in st.session_state:
    st.session_state.api_keys_set = False

# Page Configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .info-text {
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    .success-text {
        color: #0f5132;
        background-color: #d1e7dd;
        padding: 0.5rem;
        border-radius: 0.25rem;
    }
    .error-text {
        color: #842029;
        background-color: #f8d7da;
        padding: 0.5rem;
        border-radius: 0.25rem;
    }
    .warning-text {
        color: #664d03;
        background-color: #fff3cd;
        padding: 0.5rem;
        border-radius: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

def update_progress(increment: float, status: str):
    """Update the progress bar and status message."""
    st.session_state.progress += increment
    st.session_state.status = status
    if st.session_state.progress > 1.0:
        st.session_state.progress = 1.0

class StreamlitLogger:
    """Custom logger class to capture output for Streamlit."""
    
    def __init__(self, placeholder):
        self.placeholder = placeholder
        self.logs = []
        
    def log(self, message):
        """Log a message to the Streamlit app."""
        self.logs.append(message)
        self.placeholder.markdown('\n'.join(self.logs))
        
    def clear(self):
        """Clear the logs."""
        self.logs = []
        self.placeholder.markdown('')

def display_analyst_info(analyst_dict):
    """Display analyst information in a nicely formatted way."""
    st.markdown(f"**Name:** {analyst_dict['name']}")
    st.markdown(f"**Affiliation:** {analyst_dict['affiliation']}")
    st.markdown(f"**Role:** {analyst_dict['role']}")
    st.markdown(f"**Description:** {analyst_dict['description']}")
    st.markdown("---")

# Main app container
st.markdown("<div class='main-header'>AI Research Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='info-text'>Generate comprehensive research reports on any topic using AI agents and experts.</div>", unsafe_allow_html=True)

# Sidebar - API Keys and Configuration
with st.sidebar:
    st.markdown("<div class='sub-header'>API Configuration</div>", unsafe_allow_html=True)

    # LLM Provider Selection
    st.markdown("<div class='sub-header'>LLM Provider</div>", unsafe_allow_html=True)
    llm_provider = st.radio(
        "Select LLM Provider",
        options=["Azure OpenAI", "OpenAI", "Groq", "Anthropic"],
        index=0,
        help="Choose which LLM provider to use for the research assistant"
    )
    
    # Initialize variables to store in session state
    if "api_keys_set" not in st.session_state:
        st.session_state.api_keys_set = False
    
    # Display appropriate API key inputs based on selection
    if llm_provider == "Azure OpenAI":
        st.markdown("### Azure OpenAI Configuration")
        # API Key Input
        azure_openai_key = st.text_input("Azure OpenAI API Key", value=AZURE_OPENAI_API_KEY, type="password", help="Your Azure OpenAI API key")
        azure_openai_endpoint = st.text_input("Azure OpenAI Endpoint", value=AZURE_OPENAI_ENDPOINT, help="Your Azure OpenAI endpoint URL")
        azure_openai_api_version = st.text_input("Azure OpenAI API Version", value=AZURE_OPENAI_API_VERSION, help="API version for Azure OpenAI")
        azure_openai_deployment = st.text_input("Azure OpenAI Deployment", value=AZURE_OPENAI_DEPLOYMENT, help="Deployment name for your Azure OpenAI model")
        # Azure OpenAI configuration will be shown below
    elif llm_provider == "OpenAI":
        st.markdown("### OpenAI Configuration")
        openai_api_key = st.text_input("OpenAI API Key", type="password", help="Your OpenAI API key")
        openai_model = st.selectbox(
            "OpenAI Model",
            options=["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
            index=0,
            help="Select which OpenAI model to use"
        )
    elif llm_provider == "Groq":
        st.markdown("### Groq Configuration")
        groq_api_key = st.text_input("Groq API Key", type="password", help="Your Groq API key")
        groq_model = st.selectbox(
            "Groq Model",
            options=["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"],
            index=0,
            help="Select which Groq model to use"
        )
    elif llm_provider == "Anthropic":
        st.markdown("### Anthropic Configuration")
        anthropic_api_key = st.text_input("Anthropic API Key", type="password", help="Your Anthropic API key")
        anthropic_model = st.selectbox(
            "Anthropic Model",
            options=["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
            index=1,
            help="Select which Anthropic model to use"
        )
    
    # Store the selected provider in session state
    st.session_state.llm_provider = llm_provider
    
    
    
    tavily_api_key = st.text_input("Tavily API Key", value=TAVILY_API_KEY, type="password", help="Your Tavily API key for web search")
    
    # Save API Keys button
    if st.button("Save API Keys"):
        if azure_openai_key and azure_openai_endpoint and tavily_api_key:
            # Set environment variables
            os.environ["AZURE_OPENAI_API_KEY"] = azure_openai_key
            os.environ["AZURE_OPENAI_ENDPOINT"] = azure_openai_endpoint
            os.environ["AZURE_OPENAI_API_VERSION"] = azure_openai_api_version
            os.environ["AZURE_OPENAI_DEPLOYMENT"] = azure_openai_deployment
            os.environ["TAVILY_API_KEY"] = tavily_api_key
            
            st.session_state.api_keys_set = True
            st.sidebar.success("API keys saved successfully!")
        else:
            st.sidebar.error("Please provide all required API keys")
    
    st.divider()
    
    # Research parameters
    st.markdown("<div class='sub-header'>Research Parameters</div>", unsafe_allow_html=True)
    
    research_topic = st.text_area("Research Topic", value=DEFAULT_RESEARCH_TOPIC, help="Topic to research")
    num_analysts = st.slider("Number of Analysts", min_value=1, max_value=5, value=DEFAULT_NUM_ANALYSTS, help="Number of analyst agents to generate")
    max_turns = st.slider("Interview Turns", min_value=1, max_value=10, value=DEFAULT_MAX_INTERVIEW_TURNS, help="Maximum conversation turns per interview")
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=DEFAULT_MODEL_TEMPERATURE, step=0.1, help="Model temperature (higher = more creative)")
    
    # Start Research button
    start_research = st.button("Start Research Process", type="primary", use_container_width=True)

# Main content area
tab1, tab2, tab3 = st.tabs(["Research Process", "Generated Report", "Analyst Profiles"])

# Progress tracking
progress_bar = tab1.progress(st.session_state.progress)
status_text = tab1.empty()
if st.session_state.status:
    status_text.markdown(f"**Status:** {st.session_state.status}")

# Log area
log_placeholder = tab1.empty()
streamlit_logger = StreamlitLogger(log_placeholder)


# Main research process
async def run_research_process():
    try:
        # Set temperature as environment variable
        os.environ["DEFAULT_MODEL_TEMPERATURE"] = str(temperature)
        
        output_file = f"research_report.md"
        st.session_state.report_filename = output_file
        
        # Initialize research assistant
        update_progress(0.1, "Initializing research assistant...")
        assistant = ResearchAssistant()
        assistant.set_topic(research_topic, num_analysts, max_turns)
        
        # Generate analysts
        update_progress(0.1, "Generating analysts...")
        streamlit_logger.log("\nGenerating analysts for your research topic...")
        analysts = assistant.generate_analysts()
        
        if not analysts:
            streamlit_logger.log("❌ Failed to generate analysts. Please check your API keys and try again.")
            update_progress(0, "Failed to generate analysts")
            return
        
        # Store the analysts in session state IMMEDIATELY after generation
        st.session_state.analysts = analysts

        tab3.markdown(f"<div style='color:gray;font-size:1.0em;'>Total number of analysts: {len(st.session_state.analysts)}</div>", unsafe_allow_html=True)
    
        for analyst in st.session_state.analysts:
            tab3.markdown(f"**Name:** {analyst.name}")
            tab3.markdown(f"**Affiliation:** {analyst.affiliation}")
            tab3.markdown(f"**Role:** {analyst.role}")
            tab3.markdown(f"**Description:** {analyst.description}")
            tab3.markdown("---")
        
        streamlit_logger.log(f"\n✅ Generated {len(analysts)} analysts successfully!")
        streamlit_logger.log(" View the 'Analyst Profiles' tab to see your research team.")
        
        # Force a minimal rerun to update the UI with the analysts
        with st.spinner("Updating analyst profiles..."):
            time.sleep(0.5)  # Small delay to ensure state updates

        # Conduct interviews and generate report
        update_progress(0.3, "Conducting interviews and research...")
        streamlit_logger.log("\nStarting interviews with experts...")
        
        report = await assistant.conduct_interviews_and_generate_report(output_file)
        
        if not report:
            streamlit_logger.log("❌ Failed to generate report. Check logs for details.")
            update_progress(0, "Failed to generate report")
            return
        
        # Store the report content
        st.session_state.report_content = report
        st.session_state.research_complete = True

        # Create a container for the report content
        report_container = tab2.container()
        
        # Header for the report section
        report_container.markdown("### Generated Research Report")
        
        # Display the full report content
        report_container.markdown(st.session_state.report_content)
        
        # Add some space before the download button
        report_container.markdown("---")
        
        # Download button at the end of the report
        report_container.download_button(
            label="Download Report",
            data=st.session_state.report_content,
            file_name=st.session_state.report_filename,
            mime="text/markdown",
            use_container_width=True,
        )

        # Update progress
        update_progress(1.0, "Research complete!")
        streamlit_logger.log("\n✅ Research complete! Report generated successfully.")
        streamlit_logger.log(" View the 'Generated Report' tab to see and download your report.")
        
        
    except Exception as e:
        streamlit_logger.log(f"❌ Error during research process: {str(e)}")
        logger.error(f"Error in research process: {str(e)}")
        update_progress(0, f"Error: {str(e)}")
        
        if "429" in str(e) or "rate limit" in str(e).lower():
            streamlit_logger.log("⚠️ You've hit the Azure OpenAI rate limit. Try the following:")
            streamlit_logger.log("1. Wait a few minutes before trying again")
            streamlit_logger.log("2. Reduce the number of analysts")
            streamlit_logger.log("3. Reduce the conversation turns")
            streamlit_logger.log("4. Consider upgrading your Azure OpenAI tier")

# Trigger research process
if start_research:
    if not st.session_state.api_keys_set and not (azure_openai_key and azure_openai_endpoint and tavily_api_key):
        st.error("Please save your API keys before starting the research process")
    else:
        # Reset state
        st.session_state.research_complete = False
        st.session_state.report_content = ""
        st.session_state.analysts = []
        st.session_state.progress = 0
        streamlit_logger.clear()
        
        # Run research process
        streamlit_logger.log(f"🚀 Starting research on: {research_topic}")
        streamlit_logger.log(f"- Analysts: {num_analysts}")
        streamlit_logger.log(f"- Max interview turns: {max_turns}")
        streamlit_logger.log(f"- Temperature: {temperature}")
        
        streamlit_logger.log("\nThis process may take few seconds. Please be patient...")
        
        # Create a placeholder for the running process
        with st.spinner("Research in progress..."):
            # Need to use the asyncio event loop
            asyncio.run(run_research_process())

