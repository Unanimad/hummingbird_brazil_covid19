import json
import os

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

from humming_brazil_covid19.report.models import *


def to_csv():
    print('Exporting CSV')
    values = []
    STATES = dict(Case.STATES)
    REGION = dict(Case.REGION)
    columns = [
        'date', 'region', 'state', 'cases', 'deaths'
    ]

    df = pd.DataFrame(None, columns=columns)

    cases = Case.objects.all()

    for case in cases:
        date = datetime.strftime(case.report.updated_at, '%Y-%m-%d')
        region = REGION[case.region]
        state = STATES[case.state]
        cases = case.cases
        deaths = case.deaths

        values.append(dict(zip(columns, [date, region, state, cases, deaths])))

    df = df.append(values, ignore_index=True)
    df = df.sort_values(by=['date', 'region', 'state'])
    df.to_csv('data/brazil_covid19.csv', index=False, columns=columns)

    values = []
    columns = [
        'date', 'state', 'name', 'code', 'cases', 'deaths'
    ]
    df = pd.DataFrame(None, columns=columns)

    cases = CityCase.objects.all()

    for case in cases:
        date = datetime.strftime(case.report.updated_at, '%Y-%m-%d')

        cases = case.cases
        deaths = case.deaths
        state = STATES[case.state]
        code = case.code
        name = case.name

        values.append(dict(zip(columns, [date, state, name, code, cases, deaths])))

    df = df.append(values, ignore_index=True)
    df = df.sort_values(by=['date', 'state', 'name'])
    df.to_csv('data/brazil_covid19_cities.csv', index=False, columns=columns)


def add_rows_gsheet():
    print('Exporting to Google Sheet')
    service_account_info = json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON'))

    values = []
    STATES = dict(Case.STATES)
    REGION = dict(Case.REGION)

    credentials = ServiceAccountCredentials.from_json(service_account_info)
    client = gspread.authorize(credentials)

    work_sheet = client.open('brazil_covid19').get_worksheet(0)

    last_report = Report.objects.last()
    cases = Case.objects.filter(report=last_report)

    for case in cases:
        date = datetime.strftime(case.report.updated_at, '%Y-%m-%d')
        region = REGION[case.region]
        state = STATES[case.state]
        cases = case.cases
        deaths = case.deaths

        values.append([date, region, state, cases, deaths])

    work_sheet.append_rows(values)
