from django.core.management.base import BaseCommand

from humming_brazil_covid19.report.utils import to_csv


class Command(BaseCommand):
    help = 'Export a dataset with the last cases of COVID-19 in Brazil.'

    def handle(self, *args, **options):
        print('Job started! Wait the job end!')

        to_csv()
