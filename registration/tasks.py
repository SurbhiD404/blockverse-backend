import logging
from celery import shared_task
from django.db import transaction

from .email_service import send_registration_email
from .models import Team

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def send_email_task(self, team_id, raw_password):
    """
    Background task to send registration email safely.

    Features:
    - Retries 3 times on failure
    - Waits 10 seconds between retries
    - Never crashes Celery worker
    - Tracks email status in database
    """

    try:
        
        team = Team.objects.get(id=team_id)

        
        send_registration_email(team, raw_password)

        
        with transaction.atomic():
            team.email_sent = True
            team.save(update_fields=["email_sent"])

        logger.info(f"Email sent successfully to Team {team_id}")

    except Team.DoesNotExist:
        
        logger.error(f"Team {team_id} does not exist. Skipping task.")
        return

    except Exception as e:
        logger.error(f"Email failed for Team {team_id}: {e}")

        
        try:
            team = Team.objects.get(id=team_id)
            team.email_sent = False
            team.save(update_fields=["email_sent"])
        except Team.DoesNotExist:
            pass

        
        raise self.retry(exc=e)
