import os
import configparser
from git_repository import GitRepository

def repo_path(repo, *args):
    """Compute path under repo's gitdir

    Args:
        repo (GitRepository): git repository
        *args (string): path components

    Returns:
        string: path
    """
    return os.path.join(repo.gitdir, *args)

def repo_file(repo, *path, mkdir= False):
    """Returns the path to a file in a git repository or creates it

    Args:
        repo (_type_): _description_
        mkdir (bool, optional): _description_. Defaults to False.
    """
    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return os.path.join(repo.worktree, *path)
    
def repo_dir(repo, *path, mkdir=False):
    """Returns the path computed, can create it if non existent

    Args:
        repo (GitRepository): a git repository
        *path (list): path components
        mkdir (bool, optional): whether the method will create the directory or not. Defaults to False.
    
    Returns:
        string: path
    """
    path = repo.path(repo,*path)
    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            raise Exception(f"{path} is not a directory")
    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None

def repo_path(path):
    """Create a new repository at the provided path

    Args:
        path (string): path

    Returns:
        GitRepository: git repository
    """
    repo = GitRepository(path,True)
    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception(f"{path} is not a directory")
        if os.path.exists(repo.gitdit) and os.listdir(repo.gitdir):
            raise Exception(f"{path} is not empty")
    else:
        os.makedirs(repo.worktree)
    
    assert repo_dir(repo,"branches",mkdir=True)
    assert repo_dir(repo,"objects",mkdir=True)
    assert repo_dir(repo,"refs","tags",mkdir=True)
    assert repo_dir(repo,"refs","heads",mkdir=True)
    
    with open(repo_file(repo,"description"),"W") as f:
        f.write("Unnamed repository; edit this file 'description' to name the repository.\n")
    with open(repo_file(repo,"HEAD"),"W") as f:
        f.write("ref: refs/heads/master\n")
    with open(repo_file(repo,"config"),"W") as f:
        config = repo_default_config()
        config.write(f)
    return repo

def repo_default_config():
    ret = configparser.ConfigParser()
    ret.add_section("core")
    ret.set("core","repositoryformatversion","0")
    ret.set("core","filemode","false")
    ret.set("core","bare","false")
    return ret  