from datetime import datetime

from django.db import models
from kaggle.api.kaggle_api_extended import KaggleApi


class Kaggle(models.Model):
    last_update = models.DateTimeField(auto_now=False)

    def update_kaggle(self, folder, last_update):
        self.last_update = last_update
        self.save()

        api = KaggleApi()
        api.authenticate()

        last_update = datetime.strftime(self.last_update, "%m/%d/%Y %H:%M")
        api.dataset_create_version(
            folder, f"Auto update - {last_update} GMT-3", delete_old_versions=True
        )


class Report(models.Model):
    updated_at = models.DateTimeField(auto_now=False)

    def __str__(self):
        return self.updated_at.strftime("%d/%m/%Y")


class Case(models.Model):
    STATES = [
        ("RO", "Rondônia"),
        ("AC", "Acre"),
        ("AM", "Amazonas"),
        ("RR", "Roraima"),
        ("PA", "Pará"),
        ("AP", "Amapá"),
        ("TO", "Tocantins"),
        ("MA", "Maranhão"),
        ("PI", "Piauí"),
        ("CE", "Ceará"),
        ("RN", "Rio Grande do Norte"),
        ("PB", "Paraíba"),
        ("PE", "Pernambuco"),
        ("AL", "Alagoas"),
        ("SE", "Sergipe"),
        ("BA", "Bahia"),
        ("MG", "Minas Gerais"),
        ("ES", "Espírito Santo"),
        ("RJ", "Rio de Janeiro"),
        ("SP", "São Paulo"),
        ("PR", "Paraná"),
        ("SC", "Santa Catarina"),
        ("RS", "Rio Grande do Sul"),
        ("MS", "Mato Grosso do Sul"),
        ("MT", "Mato Grosso"),
        ("GO", "Goiás"),
        ("DF", "Distrito Federal"),
    ]

    REGION = [
        ("NE", "Nordeste"),
        ("NO", "Norte"),
        ("CO", "Centro-Oeste"),
        ("SU", "Sul"),
        ("SE", "Sudeste"),
    ]

    state = models.CharField(max_length=2, choices=STATES)
    region = models.CharField(max_length=2, choices=REGION)

    cases = models.PositiveIntegerField(default=0)
    deaths = models.PositiveIntegerField(default=0)

    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.state} {self.report}"

    class Meta:
        ordering = ["report", "state"]
        verbose_name = "Caso"


class MacroCase(models.Model):
    cases = models.PositiveIntegerField(default=0)
    deaths = models.PositiveIntegerField(default=0)
    recovered = models.PositiveIntegerField(default=0)
    monitoring = models.PositiveIntegerField(default=0)
    week = models.PositiveSmallIntegerField(default=0)

    report = models.ForeignKey(Report, on_delete=models.CASCADE)


class CityCase(models.Model):
    UF_CODE = {
        "76": "BR", "11": "RO", "12": "AC",
        "13": "AM", "14": "RR", "15": "PA",
        "16": "AP", "17": "TO", "21": "MA",
        "22": "PI", "23": "CE", "24": "RN",
        "25": "PB", "26": "PE", "27": "AL",
        "28": "SE", "29": "BA", "31": "MG",
        "32": "ES", "33": "RJ", "35": "SP",
        "41": "PR", "42": "SC", "43": "RS",
        "50": "MS", "51": "MT", "52": "GO",
        "53": "DF", }
    state = models.CharField(max_length=2, choices=Case.STATES)
    name = models.TextField()
    code = models.PositiveIntegerField()

    cases = models.PositiveIntegerField(default=0)
    deaths = models.PositiveIntegerField(default=0)

    report = models.ForeignKey(Report, on_delete=models.CASCADE)