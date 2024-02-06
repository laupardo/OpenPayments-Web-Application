from django_cron import CronJobBase, Schedule
from paymentswebapp.utils import import_payments_data

class OpenPaymentsImportJob(CronJobBase):
    #every 24 hours
    RUN_EVERY_MINS = 1440  # Set the interval in minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'paymentswebapp.OpenPaymentsImportJob'

    def do(self):
        import_payments_data()