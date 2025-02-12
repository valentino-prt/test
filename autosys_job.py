class AutosysJob:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.content = self.load_file()  # Charger le contenu au moment de l'instanciation
        self.name = self.get_job_name()
        self.type = self.get_job_type()
        self.conditions = self.get_conditions()
        self.dependencies = self.get_dependencies()

    def load_file(self) -> str:
        """Loads the JIL file content into memory."""
        try:
            with open(self.file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found.")
            return ""

    def get_job_name(self) -> str:
        """Extracts the job name from the JIL file."""
        for line in self.content.splitlines():
            if line.startswith("insert_job:"):
                return line.split()[1]
        return ""

    def get_job_type(self) -> str:
        """Extracts the job type (box, command, etc.)."""
        for line in self.content.splitlines():
            if line.startswith("job_type:"):
                return line.split()[1]
        return ""

    def get_conditions(self) -> list:
        """Retrieves conditions from the job."""
        conditions = []
        for line in self.content.splitlines():
            if line.startswith("condition:"):
                conditions.append(line.split(":", 1)[1].strip())
        return conditions

    def get_dependencies(self) -> list:
        """Finds dependencies linked to the job (if conditions contain job dependencies)."""
        dependencies = []
        for condition in self.conditions:
            dependencies.extend([word for word in condition.split() if word.startswith("job(")])
        return dependencies

    def remove_condition(self):
        """Removes conditions from the job before updating it."""
        self.content = "\n".join(
            line for line in self.content.splitlines() if not line.startswith("condition:")
        )

    def save_changes(self):
        """Saves modifications back to the file."""
        with open(self.file_path, "w") as file:
            file.write(self.content)
