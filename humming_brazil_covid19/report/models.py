from django.db import models


class Report(models.Model):
    updated_at = models.DateTimeField(auto_now=False)
