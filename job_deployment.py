
from autosys_job import  Job

if __name__ == "__main__":
    # logger = logging.getLogger('autosys_job_deployment')  # Utiliser le même logger
    #
    # logger.info("Starting deployment process...")
    #
    # try:
    #     job = AutosysJob("path/to/job.jil")
    #     logger.info(f"Deploying job {job.name} of type {job.type}")
    #     # Ajouter plus de logiques ici pour effectuer le déploiement, etc.
    #     logger.info(f"Job {job.name} deployed successfully")
    # except Exception as e:
    #     logger.error(f"Error during job deployment: {str(e)}")
    job = Job.from_jil_file("/Users/val/Coding/Repositories/test/file_watcher.jil")
    print(job)
    job.to_jil_file("/Users/val/Coding/Repositories/test/file_watcher2.jil")