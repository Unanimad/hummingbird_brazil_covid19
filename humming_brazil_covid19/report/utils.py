from datetime import datetime

import pandas as pd

from humming_brazil_covid19.report.models import *


def to_csv():
    values = []
    STATES = dict(Case.STATES)
    columns = [
        'date', 'hour', 'state', 'suspects', 'refuses', 'cases', 'deaths'
    ]

    df = pd.read_csv('data/brazil_covid19.csv', usecols=columns)

    reports = Report.objects.all()

    for report in reports:
        date = datetime.strftime(report.updated_at, '%Y-%m-%d')
        hour = datetime.strftime(report.updated_at, '%H:%M')

        temp = df.loc[(df.date == date) & (df.hour == hour)]
        if temp.empty:
            cases = Case.objects.filter(report=report)
            for case in cases:
                state = STATES[case.state]
                suspects = case.suspects
                refuses = case.refuses
                cases = case.cases
                deaths = case.deaths

                values.append(dict(zip(columns, [date, hour, state, suspects, refuses, cases, deaths])))

                print(values)

    df = df.append(values, ignore_index=True)
    df = df.sort_values(by=['date', 'hour', 'state'])
    df.to_csv('data/brazil_covid19.csv', index=False, columns=columns)
