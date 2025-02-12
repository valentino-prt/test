import os
from typing import List

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
        """Runs git diff to track changes."""
        result = subprocess.run(
            ["git", "-C", self.repo_path, "diff", "--name-status", "HEAD~1"],
            capture_output=True, text=True
        )
        return [line.split("\t")[1] for line in result.stdout.split("\n") if line.startswith(status)]
