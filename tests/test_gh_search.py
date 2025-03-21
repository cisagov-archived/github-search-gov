"""Tests for gh_search."""

# Standard Python Libraries
import os
import warnings

# Third-Party Libraries
import pytest

# cisagov Libraries
import gh_search

# define sources of version strings
RELEASE_TAG = os.getenv("RELEASE_TAG")
PROJECT_VERSION = gh_search.__version__


@pytest.mark.skipif(
    RELEASE_TAG in [None, ""], reason="this is not a release (RELEASE_TAG not set)"
)
def test_release_version():
    """Verify that release tag version agrees with the module version."""
    assert (
        RELEASE_TAG == f"v{PROJECT_VERSION}"
    ), "RELEASE_TAG does not match the project version"


def test_warn_project():
    """Emit a warning indicating the project lacks thorough testing."""
    warnings.warn("This project is not well-tested", UserWarning)
    # The assertion below ensures the test passes.
    assert True
