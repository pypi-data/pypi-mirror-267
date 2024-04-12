# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Unit tests for create_local_venv function to test the
deletion of the local virtual environment.

"""
from unittest.mock import MagicMock, patch

import pytest

from qbraid_core.exceptions import RequestsApiError
from qbraid_core.services.environments.client import EnvironmentManagerClient
from qbraid_core.services.environments.exceptions import EnvironmentServiceRequestError


@pytest.fixture
def mock_qbraid_session():
    """A fixture to mock qBraid session."""
    with patch("qbraid_core.session.QbraidSession", autospec=True) as mock:
        # Mock the necessary session methods here, e.g., get_user
        mock.return_value.get_user.return_value = {
            "personalInformation": {"organization": "qbraid", "role": "guest"}
        }
        yield mock


def test_delete_environment_with_valid_session():
    """Test deleting an environment with a valid session."""
    with patch("requests.Session.delete") as mock_delete:
        # Assuming delete_environment method successfully calls the session's delete method
        mock_delete.return_value = MagicMock(status_code=204)  # Simulate successful deletion

        client = EnvironmentManagerClient()  # Initializes with a valid mocked QbraidSession
        slug = "valid_slug12"
        client.delete_environment(slug)  # Attempt to delete an environment

        mock_delete.assert_called_once_with(f"/environments/{slug}")


def test_delete_environment_request_failure():
    """Test environment deletion handling when the delete request fails."""
    slug = "valid_slug12"
    with patch("requests.Session.delete") as mock_delete:
        mock_delete.side_effect = RequestsApiError("API request failed")

        client = EnvironmentManagerClient()  # Initializes with a valid mocked QbraidSession
        with pytest.raises(EnvironmentServiceRequestError):
            client.delete_environment(slug)

        mock_delete.assert_called_once_with(f"/environments/{slug}")
