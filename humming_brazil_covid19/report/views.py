import json

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer
from rest_framework.viewsets import ModelViewSet, ViewSetMixin

from humming_brazil_covid19.report.models import Case
from humming_brazil_covid19.report.serializers import CaseSerializer, AllCaseSerializer


class BaseModelReportViewSet(ModelViewSet):
    http_method_names = ["get"]
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "deaths": ["gte", "lte"],
        "cases": ["gte", "lte"],
        "report__updated_at": ["gte", "lte"],
        "state": ["exact"],
        "region": ["exact"],
    }


class AllCasesViewSet(BaseModelReportViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer


class LastCasesViewSet(BaseModelReportViewSet):
    queryset = Case.last_cases()
    serializer_class = AllCaseSerializer


class StatesList(ViewSetMixin):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        return Response(json.dump(Case.STATES))
