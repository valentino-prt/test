import os
from typing import List
import subprocess

class GitHubChangeTracker:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def get_changed_files(self) -> dict:
        """Returns a dict with 'added', 'modified', and 'deleted' files."""
        added = self._get_files_by_status("A")
        modified = self._get_files_by_status("M")
        deleted = self._get_files_by_status("D")
        return {"added": added, "modified": modified, "deleted": deleted}

    def _get_files_by_status(self, status: str) -> List[str]:
            """Runs git diff to track changes by status (e.g., D for deleted)."""
            # Run git diff command to get changed files
            result = subprocess.run(
                ["git", "-C", self.repo_path, "diff", "--name-only", "--diff-filter={}".format(status), "main"],
                capture_output=True, text=True
            )
            return result.stdout.splitlines()

