# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Unit tests for qBraid core helper functions related to system executables.

"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

from qbraid_core.system.executables import get_active_python_path


def test_get_active_python_path_same_as_sys_executable():
    """
    Test that get_active_python_path() matches sys.executable when executed with
    the same Python executable.

    """
    with (
        patch("qbraid_core.system.executables.sys.executable", "/opt/conda/bin/python"),
        patch("qbraid_core.system.executables.subprocess.run") as mock_run,
    ):
        mock_run.return_value = MagicMock(returncode=0, stdout="/opt/conda/bin/python\n")

        assert get_active_python_path() == Path(
            sys.executable
        ), "The path should match sys.executable"


def test_get_active_python_path_virtualenv():
    """
    Test that get_active_python_path() returns the same path as
    `which python` in a virtual environment.

    """
    virtual_env_path = "/home/jovyan/.qbraid/environments/mynewe_kc5ixd/pyenv/bin/python"
    with (
        patch("qbraid_core.system.executables.sys.executable", "/opt/conda/bin/python"),
        patch("qbraid_core.system.executables.subprocess.run") as mock_run,
    ):
        mock_run.return_value = MagicMock(returncode=0, stdout=f"{virtual_env_path}\n")

        active_path = get_active_python_path()
        expected_path = Path(virtual_env_path)
        assert str(active_path) == str(
            expected_path
        ), "The path should match the virtual environment's Python"
