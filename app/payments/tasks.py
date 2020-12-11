from datetime import datetime

import pytz
from celery.schedules import crontab
from celery.task import periodic_task

from campaign.models import Campaign


@periodic_task(run_every=crontab(minute=0, hour=0))
def campaign_target_check():
    curr_time = datetime.now(tz=pytz.UTC)
    campaign = Campaign.objects.filter(
        end_date__lte=curr_time, )

    return
