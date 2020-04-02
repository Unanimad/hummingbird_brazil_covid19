from rest_framework import serializers
from humming_brazil_covid19.report.models import Case


class CaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Case
        fields = ("state", "region", "cases", "deaths", "updated_at")


class AllCaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Case
        fields = ("state", "region", "cases", "deaths", "updated_at")
