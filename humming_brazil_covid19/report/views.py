from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import permissions

from humming_brazil_covid19.report.models import Case
from humming_brazil_covid19.report.serializers import CaseSerializer, AllCaseSerializer


class AllCasesViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.AllowAny]


class LastCasesViewSet(viewsets.ModelViewSet):
    queryset = Case.last_cases()
    serializer_class = AllCaseSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.AllowAny]
