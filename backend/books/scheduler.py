from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django.conf import settings
import logging
from .tasks import create_fines

logger = logging.getLogger(__name__)


def start_scheduler():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        create_fines,
        trigger=CronTrigger(hour=1, minute=0),
        id="create_fines",
        max_instances=1,
        replace_existing=True,
    )

    try:
        scheduler.start()
    except Exception as e:
        logger.error(f"Error while starting scheduler: {e}")