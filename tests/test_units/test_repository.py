import pytest
import tempfile
import os
import sys
import pathlib

# Add src to Python path so we can import wyag
SRC_DIR = pathlib.Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

# NOW import wyag
from wyag.repository import GitRepository, repo_create, repo_file

class TestRepositoryCreation:
    """Test suite for Git repository creation functionality."""
    
    def test_repo_create_creates_directory_structure(self, tmp_path):
        """Test that repo_create creates the correct .git directory structure."""
        repo_path = tmp_path / "test_repo"
        
        repo = repo_create(str(repo_path))
        
        assert repo.worktree == str(repo_path)
        assert os.path.exists(repo.gitdir)
        assert os.path.isdir(repo.gitdir)
        
        required_dirs = [
            "branches",
            "objects",
            "refs/tags",
            "refs/heads"
        ]
        
        for dir_path in required_dirs:
            assert os.path.exists(os.path.join(repo.gitdir, dir_path))
            assert os.path.isdir(os.path.join(repo.gitdir, dir_path))
    
    
    def test_repo_create_creates_required_files(self, tmp_path):
        """Test that repo_create creates essential configuration files."""
        repo_path = tmp_path / "test_repo"
        
        repo = repo_create(str(repo_path))
        
        required_files = ["HEAD", "config", "description"]
        
        for file_name in required_files:
            file_path = repo_file(repo, file_name)
            assert os.path.exists(file_path)
            assert os.path.isfile(file_path)
    
    def test_repo_create_on_existing_directory_succeeds(self, tmp_path):
        """Test that repo_create works on an existing empty directory."""
        repo_path = tmp_path / "existing_dir"
        repo_path.mkdir()
        
        repo = repo_create(str(repo_path))
        assert repo is not None
    
    def test_repo_create_fails_on_non_empty_gitdir(self, tmp_path):
        """Test that repo_create fails if .git directory exists and is not empty."""
        repo_path = tmp_path / "test_repo"
        repo_path.mkdir()
        git_dir = repo_path / ".git"
        git_dir.mkdir()
        (git_dir / "existing_file").touch()
        
        with pytest.raises(Exception) as exc_info:
            repo_create(str(repo_path))
        
        assert "not empty" in str(exc_info.value)