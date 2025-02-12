import subprocess

class AutosysAPI:
    @staticmethod
    def add_job(file_path: str):
        subprocess.run(["./autosysApi.sh", file_path, "--add"], check=True)

    @staticmethod
    def delete_job(file_path: str):
        subprocess.run(["./autosysApi.sh", file_path, "--delete"], check=True)
