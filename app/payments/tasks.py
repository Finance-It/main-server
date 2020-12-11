from celery.schedules import crontab
from celery.task import periodic_task


@periodic_task(run_every=crontab(minute=0, hour=0))
def periodic_check_campaign():
    print('lol')
