from django.core.management.base import BaseCommand

from humming_brazil_covid19.report.management.commands.update_report import cron


class Command(BaseCommand):
    help = 'Update kaggle dataset with the last cases of COVID-19 in Brazil.'

    def handle(self, *args, **options):
        print('Cron started! Wait the job starts!')

        cron()
