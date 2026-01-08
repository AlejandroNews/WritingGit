import pytest
import tempfile
import os
from pathlib import Path

@pytest.fixture
def tmp_git_repo():
    """Create a temporary git repository for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir) / "test_repo"
        yield repo_path