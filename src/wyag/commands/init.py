"""Implementation of the init command."""
import os
from wyag.repository import repo_create

def cmd_init(args):
    """Initialize a new git repository."""
    repo = repo_create(args.path)
    return 0