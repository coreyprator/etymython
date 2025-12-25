"""
Etymython Figure Image Generation Module

Renaissance portrait generation for mythological figures using DALL-E 3.
"""

from .figure_prompts import (
    FIGURE_PROMPTS,
    get_all_figure_names,
    get_prompts_by_type,
    get_figure_types
)

from .generator import (
    generate_figure_image,
    generate_and_store_figure,
    generate_all_figures,
    list_generated_figures,
    get_generation_status,
    reset_generation_status
)

__all__ = [
    # Prompts
    "FIGURE_PROMPTS",
    "get_all_figure_names",
    "get_prompts_by_type",
    "get_figure_types",
    # Generator
    "generate_figure_image",
    "generate_and_store_figure",
    "generate_all_figures",
    "list_generated_figures",
    "get_generation_status",
    "reset_generation_status",
]
