# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Unit tests for the get_state function in the validation module.

"""

from unittest.mock import patch

import pytest

from qbraid_cli.jobs.validation import get_state


@patch("qbraid_cli.jobs.validation.quantum_lib_proxy_state")
def test_get_state_specific_library(mock_qbraid_jobs_state):
    """Test the get_state function for a specific library."""
    mock_qbraid_jobs_state.return_value = {
        "proxy_lib": "botocore",
        "supported": True,
        "enabled": False,
    }
    library = "braket"
    expected = {library: (True, False)}

    result = get_state(library)
    mock_qbraid_jobs_state.assert_called_once_with(library)
    assert result == expected, f"Expected state for {library} to be correctly returned"


@pytest.mark.parametrize(
    "library,mock_return,expected",
    [
        ("braket", {"proxy_lib": "botocore", "supported": True, "enabled": False}, (True, False)),
        ("test", {"proxy_lib": "other", "supported": False, "enabled": False}, (False, False)),
    ],
)
@patch("qbraid_cli.jobs.validation.quantum_lib_proxy_state")
def test_get_state_multiple_libraries(mock_qbraid_jobs_state, library, mock_return, expected):
    """Test the get_state function when there are multiple libraries."""
    mock_qbraid_jobs_state.return_value = mock_return

    result = get_state(library)
    mock_qbraid_jobs_state.assert_called_once_with(library)
    assert result == {library: expected}, f"Expected state for {library} to be correctly returned"
