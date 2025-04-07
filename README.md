# Multi-Agent Research Assistant

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A specialized platform that automates complex research tasks through a collaborative network of AI agents with human-in-the-loop interaction capabilities.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Basic Command](#basic-command)
  - [Command-line Options](#command-line-options)
  - [Web Interface](#web-interface)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Development](#development)
  - [Setting Up Development Environment](#setting-up-development-environment)
  - [Contributing Guidelines](#contributing-guidelines)
- [API Reference](#api-reference)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview

The Multi-Agent Research Assistant is an advanced research platform that orchestrates multiple AI agents to collaboratively analyze complex topics from diverse perspectives. The system automatically generates specialized analyst personas tailored to the research topic, conducts parallel interviews with these expert agents, and synthesizes their insights into a comprehensive, multi-faceted research report.

This platform employs a human-in-the-loop approach, allowing users to guide the research process, provide feedback on generated content, and steer the direction of the investigation in real-time.

## Key Features

- **Dynamic Analyst Generation**: Creates diverse, domain-specific expert personas calibrated to the research topic's requirements
- **Parallel Interview Processing**: Conducts concurrent interviews with multiple analysts for comprehensive coverage and efficiency
- **Human-in-the-Loop Workflow**: Enables user intervention, feedback integration, and directional guidance throughout the research cycle
- **Multi-Perspective Synthesis**: Consolidates diverse viewpoints into a cohesive, balanced research report
- **Extensible Search Capabilities**: Integrates with Tavily API for real-time, high-quality information retrieval
- **Asynchronous Processing**: Utilizes async/await patterns for optimized performance
- **Configurable Research Parameters**: Adjustable depth, breadth, and focus of research via command-line arguments

## System Requirements

- Python 3.8 or higher
- Internet connection (required for API calls to Azure OpenAI and Tavily)
- Azure OpenAI API key
- Tavily API key

## Installation

```bash
# Clone the repository
git clone https://github.com/1Lalit7/Multi-Agent-Research-Assistant.git
cd multi-agent-research-assistant

# Create a virtual environment (recommended)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory with the following configuration parameters:

```
# API Keys (Required)
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
TAVILY_API_KEY=your_tavily_api_key

# Optional Configuration
OPENAI_MODEL_NAME=gpt-4
MAX_ANALYSTS=5
```

You can also set these as environment variables directly in your system or provide them when prompted by the application.

## Usage

### Basic Command

Run the research assistant with default parameters:

```bash
python run_app.py
```

or

```bash
python -m src.main
```

### Command-line Options

```bash
python -m src.main --topic "Your research topic" --analysts 2 --turns 3 --output "report.md"
```

#### Available Options

| Option       | Description                              | Default Value                                |
| ------------ | ---------------------------------------- | -------------------------------------------- |
| `--topic`    | Research topic to investigate            | "The benefits of ai agent in various domain" |
| `--analysts` | Number of analyst personas to generate   | 3                                            |
| `--turns`    | Maximum conversation turns per interview | 5                                            |
| `--output`   | Output file path for the research report | "research_report.md"                         |

### Web Interface

The system also provides a web-based interface that can be launched with:

```bash
python -m run_app.py
```

## Project Structure

```
multi-agent-research/
├── src/                  # Source code
│   ├── agents/           # Agent orchestration and management
│   ├── analysts/         # Analyst generation and profile management
│   ├── config/           # Configuration and settings
│   ├── interview/        # Interview management and processing
│   ├── models/           # AI model interfaces and wrappers
│   ├── prompts/          # System prompts and templates
│   ├── report_generation/# Report creation and formatting
│   ├── search/           # Research and information retrieval tools
│   ├── utils/            # Helper utilities and common functions
│   ├── app.py            # Web application entry point
│   ├── main.py           # CLI application entry point
│   └── __init__.py       # Package initialization
├── notebooks/            # Jupyter notebooks for examples and testing
├── .env                  # Environment variables (create this file)
├── requirements.txt      # Project dependencies
├── run_app.py            # Convenience script to run the application
└── README.md             # Project documentation
```

## Architecture

The system follows a modular architecture with these key components:

1. **Research Assistant**: Core orchestrator that manages the entire research process
2. **Analyst Generator**: Creates diverse expert personas based on the research topic
3. **Interview Manager**: Conducts parallel conversations with analyst personas
4. **Research Tools**: Interfaces with external APIs for information retrieval
5. **Report Generator**: Synthesizes insights into a comprehensive report

The system leverages LangGraph for agent orchestration and LangChain for LLM interactions, implementing an asynchronous workflow for optimal performance.

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/1Lalit7/Multi-Agent-Research-Assistant.git
cd multi-agent-research-assistant

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt  # Create this file for dev dependencies


```

### Contributing Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Implement your changes following the project's coding standards
4. Add appropriate tests
5. Commit your changes using conventional commit messages
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request with a detailed description of changes

## API Reference

The system exposes a programmatic API for integration with other applications:

```python
from src.agents.research_assistant import ResearchAssistant

# Initialize the research assistant
assistant = ResearchAssistant()

# Configure and run research
assistant.set_topic("Your research topic", num_analysts=3, max_turns=5)
report = await assistant.run_research_process("output.md")
```

For detailed API documentation, refer to the inline docstrings in the source code.

## Dependencies

The project relies on these key technologies:

- **LangChain** (≥0.1.0): Foundation for language model interactions
- **LangGraph** (≥0.3.18): Agent orchestration framework
- **Azure OpenAI** (≥1.5.0): Large language model provider
- **Tavily** (≥0.2.9): Search and information retrieval
- **Pydantic** (≥2.10.6): Data validation and settings management
- **asyncio** (≥3.4.3): Asynchronous I/O for parallel processing

For a complete list, see `requirements.txt`.

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your API keys are correctly set in the `.env` file or as environment variables
2. **Connection Timeouts**: Check your internet connection or increase timeout settings in `src/config/settings.py`
3. **Memory Errors**: Reduce the number of analysts or conversation turns for systems with limited memory

For additional support, please [open an issue](https://github.com/yourusername/multi-agent-research/issues).

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) for providing the core language model tooling
- [LangGraph](https://github.com/langchain-ai/langgraph) for the agent orchestration framework
- [Azure OpenAI](https://azure.microsoft.com/en-us/services/cognitive-services/openai-service/) for language model APIs
- [Tavily](https://tavily.com/) for search capabilities
