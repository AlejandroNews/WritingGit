import os
import configparser
from typing import Optional

class GitRepository:
    """A git repository"""
    
    def __init__(self, path: str, force: bool = False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")
        self.conf: Optional[configparser.ConfigParser] = None
        
        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"The current directory is not a git repository {path}")
        
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")
        
        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Config file not found")
        
        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception(f"Unsupported repositoryformatversion: {vers}")

def repo_path(repo: GitRepository, *args) -> str:
    """Compute path under repo's gitdir."""
    return os.path.join(repo.gitdir, *args)

def repo_file(repo: GitRepository, *path, mkdir: bool = False) -> str:
    """Returns the path to a file in a git repository."""
    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)
    return None

def repo_dir(repo: GitRepository, *path, mkdir: bool = False) -> Optional[str]:
    """Returns the path computed, can create it if non existent."""
    path_str = repo_path(repo, *path)
    if os.path.exists(path_str):
        if os.path.isdir(path_str):
            return path_str
        else:
            raise Exception(f"{path_str} is not a directory")
    if mkdir:
        os.makedirs(path_str)
        return path_str
    else:
        return None

def repo_create(path: str) -> GitRepository:
    """Create a new repository at the provided path."""
    repo = GitRepository(path, True)
    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception(f"{path} is not a directory")
        if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
            raise Exception(f"{path} is not empty")
    else:
        os.makedirs(repo.worktree)
    
    assert repo_dir(repo, "branches", mkdir=True)
    assert repo_dir(repo, "objects", mkdir=True)
    assert repo_dir(repo, "refs", "tags", mkdir=True)
    assert repo_dir(repo, "refs", "heads", mkdir=True)
    
    # Create description file
    with open(repo_file(repo, "description"), "w") as f:
        f.write("Unnamed repository; edit this file 'description' to name the repository.\n")
    
    # Create HEAD file
    with open(repo_file(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")
    
    # Create config file
    with open(repo_file(repo, "config"), "w") as f:
        config = repo_default_config()
        config.write(f)
    
    return repo

def repo_default_config() -> configparser.ConfigParser:
    """Create default git configuration."""
    ret = configparser.ConfigParser()
    ret.add_section("core")
    ret.set("core", "repositoryformatversion", "0")
    ret.set("core", "filemode", "false")
    ret.set("core", "bare", "false")
    return ret

def repo_find(path: str = ".", required: bool = True) -> Optional[GitRepository]:
    """Find a git repository starting from path."""
    path = os.path.realpath(path)
    if os.path.isdir(os.path.join(path, ".git")):
        return GitRepository(path)
    
    parent = os.path.realpath(os.path.join(path, ".."))
    if parent == path:
        if required:
            raise Exception("No git directory.")
        else:
            return None
    
    return repo_find(parent, required)