from celery import shared_task

from .services import send_account_confirmation_email


@shared_task
def task_send_account_confirmation_email(user_id: int):
    return {
        'sent': send_account_confirmation_email(user_id=user_id)
    }
