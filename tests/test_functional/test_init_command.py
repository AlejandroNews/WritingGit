import subprocess
import tempfile
import os
import sys
from pathlib import Path


def test_init_command_via_cli():
    """Test init command through the CLI."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Get the project root directory
        project_root = Path(__file__).parent.parent.parent
        
        # Set PYTHONPATH to include src directory
        env = os.environ.copy()
        python_path = str(project_root / "src")
        if "PYTHONPATH" in env:
            env["PYTHONPATH"] = python_path + os.pathsep + env["PYTHONPATH"]
        else:
            env["PYTHONPATH"] = python_path
        
        # Run wyag init via python module
        result = subprocess.run(
            [sys.executable, "-m", "wyag", "init", tmpdir],
            capture_output=True,
            text=True,
            env=env,  # Pass modified environment
            cwd=project_root  # Run from project root
        )
        
        # Debug output
        print(f"\nTesting with temp directory: {tmpdir}")
        print(f"PYTHONPATH: {env.get('PYTHONPATH', 'Not set')}")
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {repr(result.stdout)}")
        print(f"Stderr: {repr(result.stderr)}")
        
        # Command should succeed
        assert result.returncode == 0, f"Command failed: {result.stderr}"
        
        # Repository should be created
        git_dir = os.path.join(tmpdir, ".git")
        assert os.path.exists(git_dir)
        assert os.path.isdir(git_dir)
        
        # Check essential git files
        assert os.path.exists(os.path.join(git_dir, "HEAD"))
        assert os.path.exists(os.path.join(git_dir, "config"))