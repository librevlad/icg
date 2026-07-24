import os
import shutil

class Workspace:
    """
    Workspace isolates the execution environment and context.
    Future features will include checkout, branch, patch, snapshot, and rollback.
    """
    
    def __init__(self, root_path: str):
        self.root_path = os.path.abspath(root_path)
        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path)

    def get_path(self, relative_path: str) -> str:
        """Resolves a relative path to the workspace root safely."""
        return os.path.join(self.root_path, relative_path)

    def read_file(self, relative_path: str) -> str:
        with open(self.get_path(relative_path), 'r', encoding='utf-8') as f:
            return f.read()

    def write_file(self, relative_path: str, content: str):
        path = self.get_path(relative_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def execute_command(self, cmd: str) -> str:
        """
        Temporarily allows running simple commands in the workspace.
        This might be delegated entirely to a Bash Node later, but useful for basic Git operations.
        """
        import subprocess
        result = subprocess.run(cmd, shell=True, cwd=self.root_path, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {result.stderr}")
        return result.stdout
