"""Simple entry point for wyag."""
import sys
import os
from wyag.cli import main

sys.path.insert(0, os.path.dirname(__file__))


if __name__ == "__main__":
    sys.exit(main())