# class AutosysJob:
#     def __init__(self, file_path: str):
#         self.file_path = file_path
#         self.content = self.load_file()  # Charger le contenu au moment de l'instanciation
#         self.name = self.get_job_name()
#         self.type = self.get_job_type()
#         self.conditions = self.get_conditions()
#         self.dependencies = self.get_dependencies()
#
#     def load_file(self) -> str:
#         """Loads the JIL file content into memory."""
#         try:
#             with open(self.file_path, "r") as file:
#                 return file.read()
#         except FileNotFoundError:
#             print(f"Error: File {self.file_path} not found.")
#             return ""
#
#     def get_job_name(self) -> str:
#         """Extracts the job name from the JIL file."""
#         for line in self.content.splitlines():
#             if line.startswith("insert_job:"):
#                 return line.split()[1]
#         return ""
#
#     def get_job_type(self) -> str:
#         """Extracts the job type (box, command, etc.)."""
#         for line in self.content.splitlines():
#             if line.startswith("job_type:"):
#                 return line.split()[1]
#         return ""
#
#     def get_conditions(self) -> list:
#         """Retrieves conditions from the job."""
#         conditions = []
#         for line in self.content.splitlines():
#             if line.startswith("condition:"):
#                 conditions.append(line.split(":", 1)[1].strip())
#         return conditions
#
#     def get_dependencies(self) -> list:
#         """Finds dependencies linked to the job (if conditions contain job dependencies)."""
#         dependencies = []
#         for condition in self.conditions:
#             dependencies.extend([word for word in condition.split() if word.startswith("job(")])
#         return dependencies
#
#     def remove_condition(self):
#         """Removes conditions from the job before updating it."""
#         self.content = "\n".join(
#             line for line in self.content.splitlines() if not line.startswith("condition:")
#         )
#
#     def save_changes(self):
#         """Saves modifications back to the file."""
#         with open(self.file_path, "w") as file:
#             file.write(self.content)


import re
from typing import Dict, Optional

class Job:
    def __init__(self, name: str, attributes: Optional[Dict[str, str]] = None):
        self.name = name
        self.attributes = attributes if attributes else {}

    @classmethod
    def from_jil_file(cls, file_path: str) -> "Job":
        """Parse a .jil file and create a Job object."""
        attributes = {}
        name = None
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("/*"):  # Ignore empty lines and comments
                    continue

                # Trouver toutes les paires clé: valeur
                matches = re.findall(r'(\w+):\s*("[^"]*"|\S+)', line)
                for key, value in matches:
                    attributes[key] = value.strip('"')  # Enlever les guillemets s'ils existent
                    if key.lower() == "insert_job" and not name:
                        name = value.split()[0]  # Extraire uniquement le nom du job

        if not name:
            raise ValueError("Job name (insert_job) is missing in the .jil file.")

        return cls(name, attributes)

    def to_jil_file(self, file_path: str):
        """Generate a .jil file from the Job object with exact formatting."""
        with open(file_path, "w") as file:
            insert_comment_line = f"/* ----------------- {self.name} ----------------- */\n"
            file.write(insert_comment_line + "\n")
            insert_job_line = f"insert_job: {self.name}"
            if "job_type" in self.attributes:
                insert_job_line += f"   job_type: {self.attributes['job_type']}"
            file.write(insert_job_line + "\n")

            # Écrire les autres attributs en respectant l'ordre d'origine
            for key, value in self.attributes.items():
                if key.lower() == "insert_job" or key.lower() == "job_type":
                    continue  # Déjà inclus dans la première ligne

                # Vérifier si la valeur doit être entre guillemets
                formatted_value = f'"{value}"' if " " in value or ":" in value else value
                file.write(f"{key}: {formatted_value}\n")

    def __repr__(self):
        return f"Job(name={self.name}, attributes={self.attributes})"


