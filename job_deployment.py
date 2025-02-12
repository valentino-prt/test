import logging
from autosys_job import AutosysJob


if __name__ == "__main__":
    logger = logging.getLogger('autosys_job_deployment')  # Utiliser le même logger

    logger.info("Starting deployment process...")

    try:
        job = AutosysJob("path/to/job.jil")
        logger.info(f"Deploying job {job.name} of type {job.type}")
        # Ajouter plus de logiques ici pour effectuer le déploiement, etc.
        logger.info(f"Job {job.name} deployed successfully")
    except Exception as e:
        logger.error(f"Error during job deployment: {str(e)}")
