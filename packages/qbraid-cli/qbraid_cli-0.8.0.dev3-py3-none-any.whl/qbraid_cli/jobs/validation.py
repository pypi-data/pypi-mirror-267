# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module for validating command arguments for qBraid Quantum Jobs.

"""

from typing import Callable, Dict, Optional, Tuple

import typer
from qbraid_core.services.quantum.proxy import SUPPORTED_QJOB_LIBS, quantum_lib_proxy_state
from rich.console import Console

from qbraid_cli.handlers import handle_error, run_progress_task, validate_item


def validate_library(value: str) -> str:
    """Validate quantum jobs library."""
    return validate_item(value, SUPPORTED_QJOB_LIBS, "Library")


def get_state(library: Optional[str] = None) -> Dict[str, Tuple[bool, bool]]:
    """Get the state of qBraid Quantum Jobs for the specified library."""

    state_values = {}

    if library:
        libraries_to_check = [library]
    else:
        libraries_to_check = SUPPORTED_QJOB_LIBS

    for lib in libraries_to_check:
        state = quantum_lib_proxy_state(lib)
        state_values[lib] = state["supported"], state["enabled"]

    return state_values


def run_progress_get_state(library: Optional[str] = None) -> Dict[str, Tuple[bool, bool]]:
    """Run get state function with rich progress UI."""
    return run_progress_task(
        get_state,
        library,
        description="Collecting package metadata...",
        error_message=f"Failed to collect {library} package metadata.",
    )


def handle_jobs_state(
    library: str,
    action: str,  # 'enable' or 'disable'
    action_callback: Callable[[], None],
) -> None:
    """Handle the common logic for enabling or disabling qBraid Quantum Jobs."""
    state_values: Dict[str, Tuple[bool, bool]] = run_progress_get_state(library)
    installed, enabled = state_values[library]

    if not installed:
        handle_error(message=f"{library} not installed.")
    if (enabled and action == "enable") or (not enabled and action == "disable"):
        action_color = "green" if enabled else "red"
        console = Console()
        console.print(
            f"\nqBraid quantum jobs already [bold {action_color}]{action}d[/bold {action_color}] "
            f"for [magenta]{library}[/magenta]."
        )
        console.print(
            "To check the state of all quantum jobs libraries in this environment, "
            "use: \n\n\t$ qbraid jobs state\n"
        )
        raise typer.Exit()

    action_callback()  # Perform the specific enable/disable action
