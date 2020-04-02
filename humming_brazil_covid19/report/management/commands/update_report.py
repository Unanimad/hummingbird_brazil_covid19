import json

import requests

from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler

from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand

from humming_brazil_covid19.report.management.commands.load_database import load_database
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

        last_report = datetime.strptime(data['dt_atualizacao'], '%H:%M %d/%m/%Y')

        report, created = Report.objects.get_or_create(
            updated_at=last_report
        )

        if created:
            request = requests.get(url + 'PortalMapa', headers=headers)
            content = request.content.decode('utf8')
            data = json.loads(content)['results']

            for state in data:
                state_uf = ''

                for uf in Case.STATES:
                    if uf[1] == state['nome']:
                        state_uf = uf[0]

                case = list(Case.objects.filter(state=state_uf))[0]

                cases = state.get('qtd_confirmado', 0)
                deaths = state.get('qtd_obito', 0)

                Case.objects.get_or_create(
                    cases=cases, deaths=deaths,
                    state=state_uf, region=case.region,
                    report=report
                )

            to_csv()

            instance = Kaggle.objects.last()
            if not instance:
                instance = Kaggle.objects.create(last_update=last_report)

            instance.update_kaggle('data/', last_report)

        else:
            print(f"The last report {report.updated_at} already exists!")

        print(f"Done! The time is: {datetime.now()}")
    else:
        print("It's not time yet!")


class Command(BaseCommand):
    help = 'Automatically update  kaggle dataset with the last cases of COVID-19 in Brazil.'

    def handle(self, *args, **options):
        print('Cron started! Wait the job starts!')

        scheduler = BlockingScheduler()
        scheduler.add_job(cron, 'interval', minutes=20, timezone='America/Maceio')

        scheduler.start()
