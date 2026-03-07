from celery import Celery
from celery.signals import after_setup_logger, after_setup_task_logger
import celery_config

celery_app = Celery("worker_service")
celery_app.conf.update(celery_config.CELERY_CONFIG)

@after_setup_logger.connect
def setup_celery_logger(logger, *args, **kwargs):
    logger.info("Celery logger is set up.")

@after_setup_task_logger.connect
def setup_task_logger(logger, *args, **kwargs):
    logger.info("Celery task logger is set up.")

import tasks

