"""Entry point for python -m wyag."""

import sys

# Import from the wyag package
from wyag.cli import main

if __name__ == "__main__":
    sys.exit(main())