__author__ = "Kris"
from .database import Database
from .sms import Sms

db = Database
db.initialize()

class JobSearcher(object):
    SMS_JOBS = None
    EMAIL_JOBS = None

    @staticmethod
    def search_for_sms_jobs():
        print("looking for SMS jobs to do")
        sms = Sms()
        JobSearcher.SMS_JOBS = sms.retrieve()

    @staticmethod
    def send_sms():
        jobs_to_do = JobSearcher.SMS_JOBS
        if jobs_to_do:
            print(print('found ' + str(jobs_to_do.count()) + ' job to do.'))
            for job in jobs_to_do:
                sms = Sms(message=job['message']['message'])
                sms.send()
            print("All SMS jobs complete")
        else:
            print("No SMS jobs to do")

    @staticmethod
    def search_for_email_jobs():
        print("looking for email jobs to do")
        sms = Sms()
        JobSearcher.SMS_JOBS = sms.retrieve()

    @staticmethod
    def send_emails():
        jobs_to_do = JobSearcher.SMS_JOBS
        if jobs_to_do:
            print(print('found ' + str(jobs_to_do.count()) + ' job to do.'))
            for job in jobs_to_do:
                sms = Sms(message=job['message']['message'])
                sms.send()
            print("All email jobs complete")
        else:
            print("No email jobs to do")

# jobs = JobSearcher()
#
# jobs.search_for_sms_jobs()
# jobs.send_sms()
#
# jobs.search_for_email_jobs()
# jobs.send_emails()



