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

        last_update = datetime.strftime(self.last_update, '%m/%d/%Y %H:%M')
        api.dataset_create_version(folder, f"Auto update - {last_update} GMT-3",
                                   delete_old_versions=True)


class Report(models.Model):
    updated_at = models.DateTimeField(auto_now=False)

    def __str__(self):
        return self.updated_at.strftime('%d/%m/%Y')


class Case(models.Model):
    STATES = [
        ('RO', 'Rondônia'), ('AC', 'Acre'), ('AM', 'Amazonas'), ('RR', 'Roraima'),
        ('PA', 'Pará'), ('AP', 'Amapá'), ('TO', 'Tocantins'), ('MA', 'Maranhão'),
        ('PI', 'Piauí'), ('CE', 'Ceará'), ('RN', 'Rio Grande do Norte'),
        ('PB', 'Paraíba'), ('PE', 'Pernambuco'), ('AL', 'Alagoas'),
        ('SE', 'Sergipe'), ('BA', 'Bahia'), ('MG', 'Minas Gerais'),
        ('ES', 'Espírito Santo'), ('RJ', 'Rio de Janeiro'), ('SP', 'São Paulo'),
        ('PR', 'Paraná'), ('SC', 'Santa Catarina'), ('RS', 'Rio Grande do Sul'),
        ('MS', 'Mato Grosso do Sul'), ('MT', 'Mato Grosso'), ('GO', 'Goiás'),
        ('DF', 'Distrito Federal')
    ]

    REGION = [
        ('NE', 'Nordeste'), ('NO', 'Norte'), ('CO', 'Centro-Oeste'),
        ('SU', 'Sul'), ('SE', 'Sudeste')

    ]

    state = models.CharField(max_length=2, choices=STATES)
    region = models.CharField(max_length=2, choices=REGION)

    cases = models.PositiveSmallIntegerField(default=0)
    deaths = models.PositiveSmallIntegerField(default=0)

    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.state} {self.report}"

    class Meta:
        ordering = ['report', 'state']
        verbose_name = 'Caso'
