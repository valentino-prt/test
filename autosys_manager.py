from autosys_api import AutosysAPI
from github_change_tracker import GitHubChangeTracker


class AutosysManager:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.tracker = GitHubChangeTracker(repo_path)

    def process_changes(self):
        changes = self.tracker.get_changed_files()

        for file in changes["deleted"]:
            print(f"Deleting {file} from Autosys")
            AutosysAPI.delete_job(file)

        for file in changes["added"]:
            print(f"Adding {file} to Autosys")
            AutosysAPI.add_job(file)

        for file in changes["modified"]:
            print(f"Updating {file} in Autosys")
            self.update_job(file)

    def update_job(self, file_path: str):
        job = AutosysJob(file_path)
        job.remove_condition()
        AutosysAPI.add_job(file_path)
