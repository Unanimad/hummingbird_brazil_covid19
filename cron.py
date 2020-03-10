from apscheduler.schedulers.blocking import BlockingScheduler

from main import job

scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', hour=17, timezone='America/Maceio')

scheduler.start()
