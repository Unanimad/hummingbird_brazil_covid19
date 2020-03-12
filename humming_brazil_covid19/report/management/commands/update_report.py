import json

import requests
import pandas as pd

from datetime import datetime

from kaggle.api.kaggle_api_extended import KaggleApi
from apscheduler.schedulers.blocking import BlockingScheduler

from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand

from humming_brazil_covid19.report.utils import *
from humming_brazil_covid19.report.models import *

url = "http://plataforma.saude.gov.br/novocoronavirus/resources/scripts/database.js"

STATES = {11: 'Rondônia', 12: 'Acre', 13: 'Amazonas', 14: 'Roraima', 15: 'Pará',
          16: 'Amapá', 17: 'Tocantins', 21: 'Maranhão', 22: 'Piauí', 23: 'Ceará',
          24: 'Rio Grande do Norte', 25: 'Paraíba', 26: 'Pernambuco', 27: 'Alagoas',
          28: 'Sergipe', 29: 'Bahia', 31: 'Minas Gerais', 32: 'Espírito Santo',
          33: 'Rio de Janeiro', 35: 'São Paulo', 41: 'Paraná', 42: 'Santa Catarina',
          43: 'Rio Grande do Sul', 50: 'Mato Grosso do Sul', 51: 'Mato Grosso',
          52: 'Goiás', 53: 'Distrito Federal'}


def cron(*args, **options):
    if 6 <= datetime.now().hour <= 20:

        print("Cron job is running. The time is %s" % datetime.now())
        request = requests.get(url)

        content = request.content.decode('utf8').replace('var database=', '')
        data = json.loads(content)

        last_report = f"{data['brazil'][-1]['date']} {data['brazil'][-1]['time']}"
        last_report = datetime.strptime(last_report, '%d/%m/%Y %H:%M')

        report, created = Report.objects.get_or_create(updated_at=make_aware(last_report))

        if created:
            df = pd.DataFrame(None, columns=['date', 'hour', 'state',
                                             'suspects', 'refuses', 'cases'])

            for record in data['brazil']:
                confirmed_at = datetime.strptime(record['date'], '%d/%m/%Y')
                confirmed_at = datetime.strftime(confirmed_at, '%Y-%m-%d')
                hour = record['time']

                for value in record['values']:
                    state = STATES[int(value['uid'])]

                    suspects = get_key_value('suspects', value)
                    refuses = get_key_value('refuses', value)
                    cases = get_key_value('cases', value)

                    df = df.append(dict(zip(df.columns, [confirmed_at, hour, state,
                                                         suspects, refuses, cases])),
                                   ignore_index=True)

            df.to_csv('data/brazil_covid19.csv', index=False)

            report.updated_at = make_aware(last_report)
            report.save()

            update_dataset('data/',
                           f"Auto update - {datetime.strftime(datetime.now(), '%m/%d/%Y %H:%M')}")

            print("Successful data uploaded to Kaggle!")

        else:
            print(f"The last report {last_report} already exists!")

        print("Done! The time is: %s" % datetime.now())


def update_dataset(folder, note):
    api = KaggleApi()
    api.authenticate()

    return api.dataset_create_version(folder, note, delete_old_versions=True)


class Command(BaseCommand):
    help = 'Update kaggle dataset with the last cases of COVID-19 in Brazil.'

    def handle(self, *args, **options):
        print('Cron started! Wait the job starts!')

        scheduler = BlockingScheduler()
        scheduler.add_job(cron, 'interval', minutes=20, timezone='America/Maceio')

        scheduler.start()
