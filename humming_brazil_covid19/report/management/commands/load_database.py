import json

import pandas as pd
import requests

from django.core.management.base import BaseCommand

from humming_brazil_covid19.report.models import *

url = "https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/"
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "x-parse-application-id": "unAFkcaNDeXajurGB7LChj8SgQYS2ptm"
}


def load_database(*args, **options):
    print(f"Job is running. The time is {datetime.now()}")

    request = requests.get(url + 'PortalGeral', headers=headers)

    content = request.content.decode('utf8')

    data = json.loads(content)['results'][0]

    last_platform_report = datetime.strptime(data['dt_atualizacao'], '%H:%M %d/%m/%Y')

    last_report, created = Report.objects.get_or_create(
        updated_at=last_platform_report
    )

    if created is False:
        return print(f"No updates yet! Last report was at {data['dt_atualizacao']}")

    else:
        print(f"Fetching new report: {data['dt_atualizacao']}")

        csv_file = f"https://covid.saude.gov.br/assets/files/COVID19_{datetime.strftime(last_platform_report, '%Y%m%d')}.csv"
        df = pd.read_csv(csv_file, sep=';')

        for i, row in df.iterrows():
            date = datetime.strptime(row['data'], '%d/%m/%Y')
            report, created = Report.objects.get_or_create(
                updated_at=date
            )

            cases = row['casosAcumulados']
            deaths = row['obitosAcumulado']

            default_region = ''
            for region in Case.REGION:
                if region[1] == row['regiao']:
                    default_region = region[0]
                    break

            Case.objects.get_or_create(
                cases=cases, deaths=deaths,
                state=row['estado'], region=default_region,
                report=report
            )


class Command(BaseCommand):
    help = 'Automatically load the database with the cases of COVID-19 in Brazil.'

    def handle(self, *args, **options):
        load_database()