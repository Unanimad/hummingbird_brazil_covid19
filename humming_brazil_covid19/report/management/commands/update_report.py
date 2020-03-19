import json

import requests

from datetime import datetime
from operator import itemgetter

from apscheduler.schedulers.blocking import BlockingScheduler

from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand

from humming_brazil_covid19.report.models import *

url = "http://plataforma.saude.gov.br/novocoronavirus/resources/scripts/database.js"


def cron(*args, **options):
    if 6 <= datetime.now().hour <= 20:

        print(f"Cron job is running. The time is {datetime.now()}")
        request = requests.get(url)

        content = request.content.decode('utf8').replace('var database=', '')
        data = json.loads(content)

        # last_report = f"{data['brazil'][-1]['date']} {data['brazil'][-1]['time']}"
        # last_report = datetime.strptime(last_report, '%d/%m/%Y %H:%M')

        for record in data['brazil']:
            date_time = datetime.strptime(f"{record['date']} {record['time']}",
                                          '%d/%m/%Y %H:%M')

            report, created = Report.objects.get_or_create(
                defaults={'updated_at': make_aware(date_time)}
            )

            if created:
                for value in record['values']:
                    state = list(map(itemgetter(0), Case.STATES))

                    suspects = value.get('suspects', 0)
                    refuses = value.get('refuses', 0)
                    cases = value.get('cases', 0)
                    deaths = value.get('deaths', 0)

                    Case.objects.get_or_create(
                        suspects, refuses, cases, deaths,
                        defaults={
                            'state': state,
                            'report': report
                        })

        instance = Kaggle.objects.last()
        if instance.last_update != report.last_report:
            instance.update_kaggle('data/', report.last_report)

        print(f"The last report {report.last_report} already exists!")

    print(f"Done! The time is: {datetime.now()}")


class Command(BaseCommand):
    help = 'Update kaggle dataset with the last cases of COVID-19 in Brazil.'

    def handle(self, *args, **options):
        print('Cron started! Wait the job starts!')

        scheduler = BlockingScheduler()
        scheduler.add_job(cron, 'interval', minutes=20, timezone='America/Maceio')

        scheduler.start()
