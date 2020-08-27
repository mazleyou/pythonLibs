# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError

import time


def job():
    print("I'm working...", "| [time] "
          , str(time.localtime().tm_hour) + ":"
          + str(time.localtime().tm_min) + ":"
          + str(time.localtime().tm_sec))


def job_2():
    print("Job2 실행: ", "| [time] "
          , str(time.localtime().tm_hour) + ":"
          + str(time.localtime().tm_min) + ":"
          + str(time.localtime().tm_sec))


sched = BackgroundScheduler()
sched.start()

sched.add_job(job, 'interval', seconds=3, id="test_2")

sched.add_job(job, 'cron', second='*/5', id="test_1")

sched.add_job(job_2, 'cron', minute="59", second='10', id="test_10")

count = 0
while True:
    print("Running main process...............")
    time.sleep(1)