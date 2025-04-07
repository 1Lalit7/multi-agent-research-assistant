"""
Formal Report package.

This package contains modules for generating formal research reports
based on analyst interviews and insights.
"""

# Import main report generator
from src.report_generation.report_generation_graph import build_report_generator

# Import core report functions
from src.report_generation.report_content_generator import (
    write_introduction,
    write_conclusion,
    write_report
)

from src.report_generation.report_orchestrator import (
    initiate_all_interviews,
    finalize_report
)

# Import state schema
from src.report_generation.report_schema import ResearchGraphState 