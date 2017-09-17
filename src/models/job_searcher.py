__author__ = "Kris"
from .database import Database
from .sms import Sms

db = Database
db.initialize()

class JobSearcher(object):
    SMS_JOBS = None


    @staticmethod
    def search_for_sms_jobs():
        sms = Sms()
        JobSearcher.SMS_JOBS = sms.retrieve_sms_messages()
        return JobSearcher.SMS_JOBS

    @staticmethod
    def send_sms():

        for job in JobSearcher.SMS_JOBS:
            sms = Sms(message=job['message']['message'])
            print(job['message'])
            sms.send_sms()






if JobSearcher.search_for_sms_jobs():
    JobSearcher.send_sms()
else:
    print('Their are no jobs to do')



