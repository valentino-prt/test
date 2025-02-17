import requests
import tempfile
import os


class AutosysAPI:
    """Class to interact with the Autosys API for file operations."""

    def __init__(self, base_url: str, auth_token: str = None):
        self.base_url = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}

    def add_files(self, file_paths: list) -> dict:
        """Upload multiple binary Autosys files via multipart/form-data."""
        url = f"{self.base_url}/files"
        files = {}

        # Read and prepare each file for upload
        for file_path in file_paths:
            with open(file_path, "rb") as file:
                files[file_path.split("/")[-1]] = (file_path.split("/")[-1], file, "application/octet-stream")

        response = requests.post(url, files=files, headers=self.headers)
        return response.json()

    def delete_files(self, file_names: list) -> dict:
        """Delete multiple Autosys files."""
        responses = {}

        for file_name in file_names:
            url = f"{self.base_url}/files/{file_name}"
            response = requests.delete(url, headers=self.headers)
            responses[file_name] = response.json()

        return responses


class AutosysManager:
    """High-level manager to interact with Autosys API."""

    def __init__(self, autosys_api: AutosysAPI):
        self.api = autosys_api

    def upload_jobs(self, job_files: dict):
        """Write job content to temporary binary files and upload them."""
        temp_file_paths = []

        # Write each job content to a temporary file
        for job_name, job_content in job_files.items():
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jil") as tmp_file:
                tmp_file.write(job_content.encode())  # Convert content to binary
                temp_file_paths.append(tmp_file.name)  # Save file path

        try:
            response = self.api.add_files(temp_file_paths)
            print(f"✅ Jobs uploaded: {response}")
        finally:
            # Clean up temporary files after upload
            for temp_file_path in temp_file_paths:
                os.remove(temp_file_path)

    def remove_jobs(self, file_names: list):
        """Delete multiple jobs from Autosys."""
        response = self.api.delete_files(file_names)
        print(f"🗑️ Jobs deleted: {response}")
