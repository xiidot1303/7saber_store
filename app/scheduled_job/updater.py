from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from app.scheduled_job import *
from asgiref.sync import async_to_sync
from app.scheduled_job.billz_job import *
from bot.scheduled_job import mailing
from bot.services.redis_service import save_langs_to_redis

class jobs:
    scheduler = BackgroundScheduler(timezone='Asia/Tashkent')
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    scheduler.add_job(fetch_and_cache_access_token, 'interval', days=10)
    scheduler.add_job(fetch_subcategories, 'cron', hour=2, minute=0)
    scheduler.add_job(fetch_products, 'cron', hour=2, minute=10)

    # bot
    scheduler.add_job(
        async_to_sync(mailing.send_message), 
        'interval', minutes=5)
    scheduler.add_job(save_langs_to_redis, 'interval', minutes=20)
