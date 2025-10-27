import logging

from celery import shared_task

logger = logging.getLogger(__file__)


@shared_task
def todo_dia_meia_noite():
    logger.info("Tarefa executada todo dia à meia-noite.")
