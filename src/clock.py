__author__ = "Kris"
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


def clock():
    sched = BackgroundScheduler()

    @sched.scheduled_job('interval', seconds=5)
    def timed_job():
        # print('This job is run every three minutes.')
        # print(str(datetime.now()))
        pass
    @sched.scheduled_job('cron', month='9', day="17", hour="12", minute="25-30", second="10,20,30,40,50")
    def cron_job():
        print("Hello, cron job is running")
    return sched


def repeated_job():
    print("this job will repeat every 10 minutes")