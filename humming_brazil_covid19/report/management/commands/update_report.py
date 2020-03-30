import json

import requests

from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler

from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand

from humming_brazil_covid19.report.models import *
from humming_brazil_covid19.report.utils import to_csv

url = "https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/"
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "x-parse-application-id": "unAFkcaNDeXajurGB7LChj8SgQYS2ptm"
}


def cron(*args, **options):
    if 6 <= datetime.now().hour <= 20:

        print(f"Cron job is running. The time is {datetime.now()}")
        request = requests.get(url + 'PortalGeral', headers=headers)

        content = request.content.decode('utf8')

        data = json.loads(content)['results'][0]

        dt, _, us = data['updatedAt'].partition(".")
        last_report = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')

        report, created = Report.objects.get_or_create(
            updated_at=last_report
        )

        if created:
            print(f"Fetching new report: {report.updated_at}")

            request = requests.get(url + 'PortalMapa', headers=headers)
            content = request.content.decode('utf8')
            data = json.loads(content)['results']

            for state in data:
                state_uid = 0

                for uid in Case.STATES:
                    if uid[1] == state['nome']:
                        state_uid = uid[0]
                        break

                suspects = state.get('qtd_suspeito', 0)
                refuses = state.get('qtd_descartado', 0)
                cases = state.get('qtd_confirmado', 0)
                deaths = state.get('qtd_obito', 0)

                Case.objects.get_or_create(
                    suspects=suspects, refuses=refuses,
                    cases=cases, deaths=deaths,
                    defaults={
                        'state': state_uid,
                        'report': report
                    })

            to_csv()

            instance = Kaggle.objects.last()
            if not instance:
                instance = Kaggle.objects.create(last_update=last_report)

            instance.update_kaggle('data/')

        else:
            print(f"The last report {report.updated_at} already exists!")

    print(f"Done! The time is: {datetime.now()}")


class Command(BaseCommand):
    help = 'Update kaggle dataset with the last cases of COVID-19 in Brazil.'

    def handle(self, *args, **options):
        print('Cron started! Wait the job starts!')

        cron()
        # scheduler = BlockingScheduler()
        # scheduler.add_job(cron, 'interval', minutes=20, timezone='America/Maceio')

        # scheduler.start()
