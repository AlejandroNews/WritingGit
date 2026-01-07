import os
from path_utils import repo_file
import configparser
class GitRepository:
    """A git repository"""
    
    worktree = None
    gitdir = None
    conf = None
    
    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")
        
        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"The current directory is not a git repository {path}")
        
        self.conf = configparser.ConfigParser()
        cf = repo_file(self,"config")
        
        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Config file not found")
        
        if not force:
            vers = int(self.conf.get("core","repositoryformatversion"))
            if vers != 0:
                raise Exception(f"Unsupported repositoryformatversion: {vers}")