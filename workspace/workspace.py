import os
import glob
import shutil
import hashlib
from typing import List, Dict

class Workspace:
    def __init__(self, root_path: str):
        self._root_path = os.path.abspath(root_path)
        os.makedirs(self._root_path, exist_ok=True)

    @property
    def root_path(self) -> str:
        return self._root_path

    def root(self) -> str:
        return self._root_path

    def exists(self) -> bool:
        return os.path.exists(self._root_path)

    def _safe_path(self, path: str) -> str:
        safe = os.path.abspath(os.path.join(self._root_path, path))
        if not safe.startswith(self._root_path):
            raise ValueError(f"Path traversal detected: {path}")
        return safe

    def read(self, path: str) -> str:
        with open(self._safe_path(path), 'r', encoding='utf-8') as f:
            return f.read()

    def write(self, path: str, content: str):
        safe_p = self._safe_path(path)
        os.makedirs(os.path.dirname(safe_p), exist_ok=True)
        with open(safe_p, 'w', encoding='utf-8') as f:
            f.write(content)

    def delete(self, path: str):
        safe_p = self._safe_path(path)
        if os.path.isfile(safe_p):
            os.remove(safe_p)
        elif os.path.isdir(safe_p):
            shutil.rmtree(safe_p)

    def list_files(self, pattern: str = None) -> List[str]:
        results = []
        exclude_dirs = {'.git', '__pycache__', 'venv', 'node_modules'}
        for root, dirs, files in os.walk(self._root_path):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), self._root_path)
                if not pattern or glob.fnmatch.fnmatch(rel_path, pattern):
                    results.append(rel_path)
        return results

    def find(self, text: str) -> List[str]:
        results = []
        for file in self.list_files():
            try:
                if text in self.read(file):
                    results.append(file)
            except UnicodeDecodeError:
                pass
        return results

    def snapshot(self) -> Dict[str, str]:
        snap = {}
        for file in self.list_files():
            try:
                content = self.read(file).encode('utf-8')
                snap[file] = hashlib.md5(content).hexdigest()
            except:
                pass
        return snap

    def diff(self, old_snapshot: Dict[str, str]) -> Dict[str, List[str]]:
        current = self.snapshot()
        added = [f for f in current if f not in old_snapshot]
        deleted = [f for f in old_snapshot if f not in current]
        modified = [f for f in current if f in old_snapshot and current[f] != old_snapshot[f]]
        return {"added": added, "modified": modified, "deleted": deleted}

    def apply_patch(self, path: str, patch: str):
        # Extremely basic patch application MVP
        self.write(path, patch)
